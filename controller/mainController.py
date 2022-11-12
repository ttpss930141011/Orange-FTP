import os
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox
import re
from os import listdir
from os.path import isfile, join
from lib.ftplib import FTP,error_perm
from pubsub import pub
from views.UI import Main_Window
from sys import exit

class Window(QMainWindow,Main_Window):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initLogMode()
        self.__initControl()
        self.__initFtp()
        self.__bindFtpMessageListener()
        self.__autoUpload()
        
    # initial data
    def __initVal(self):
        ftpHost,ftpPath,ftpAccount,ftpPassword,autoUpload,targetFilePath = self.getConfigData()
        # 自動帶入setting.txt
        self.ftpHostInput.setText(ftpHost)
        self.ftpPathInput.setText(ftpPath)
        self.ftpAccountInput.setText(ftpAccount)
        self.ftpPasswordInput.setText(ftpPassword)
        self.autoUpload = True if autoUpload and autoUpload.strip().lower() == 'yes' else False
        self.logFile = None
        self.targetFilePath = self.__ensureLocalDir(targetFilePath)
        if self.targetFilePath is not None:
            # 自動帶入file folder 內的檔案 
            for file in listdir(self.targetFilePath): 
                if isfile(join(self.targetFilePath, file)) and not self.__isTempFile(file):
                    self.FileList.setFileName(join(self.targetFilePath, file))

    # initial lot mode，依據是否為auto upload 模式去選擇是否要生成ftp.log file
    def __initLogMode(self):
        if self.autoUpload == True:
            self.logFile = open("ftp.log", "a")

    # initial button binding
    def __initControl(self):
        self.DialogButtonBox.accepted.connect(self.StartToUpload)
        self.DialogButtonBox.rejected.connect(self.__onCancelAndExit)
    
    # initial FTP connect
    def __initFtp(self):
        self.__rstripFormData()
        vaildResult = self.__validFormData()
        host = self.ftpHostInput.text()
        username = self.ftpAccountInput.text()
        password = self.ftpPasswordInput.text()
        if vaildResult:
            try:
                self.ftp = self.__ftpConnect(host,username,password)
                welComeMsg = self.ftp.getwelcome()
                self.__appendTextInFtpMsgBrower(welComeMsg)
            except:
                self.__appendTextInFtpMsgBrower(f'*error* \'Login error\'')
                self.ftp = None
    
    # main function
    def StartToUpload(self):
        self.__initFtp()
        self.__rstripFormData()
        vaildResult = self.__validFormData()
        if self.ftp is None: 
            self.__appendTextInFtpMsgBrower(f'*error* \'FTP initial error\'')
            return
        if vaildResult:
            path = self.ftpPathInput.text()
            self.__ensureRemoteDir(path)
            uploadFileAbsPathList = self.FileList.getFileName()
            self.__appendTextInFtpMsgBrower('----- Start to upload -----')
            for localPath in uploadFileAbsPathList:
                self.__uploadFile(localPath)
                self.__appendTextInFtpMsgBrower(f'*uploading* \'{os.path.basename(localPath)}\'')
            self.__appendTextInFtpMsgBrower('----- upload complete -----')
    
    # 取得 config.txt 內容
    def getConfigData(self):
        ftpHost = ftpPath = ftpAccount = ftpPassword = autoUpload = targetFilePath = ''
        try:
            config = open('config.txt', 'r')
            ftpHost = re.findall(
                r'[0-9]+(?:\.[0-9]+){3}',
                config.readline().split(':')[1])[0]
            _, _, ftpPath = config.readline().partition("FTP_Path:")
            _, _, ftpAccount = config.readline().partition("FTP_Account:")
            _, _, ftpPassword = config.readline().partition("FTP_Password:")
            _, _, autoUpload = config.readline().partition("Auto_Upload:")
            _, _, targetFilePath = config.readline().partition("Target_Filepath:")
        except:
            self.__appendTextInFtpMsgBrower(f'*error* \'Get config.txt data error\'')

        return ftpHost,ftpPath,ftpAccount,ftpPassword,autoUpload,targetFilePath

    # 依據是否為autoupload mode去自動上傳
    def __autoUpload(self):
        if self.autoUpload == True:
            self.StartToUpload()
            self.__onCancelAndExit()
            exit(0)

    # 判斷是否為temp file     
    def __isTempFile(self,file):
        _, file_extension = os.path.splitext(file)
        if file_extension != '.temp' and file_extension != '.tmp':
            return False
        else:
            return True

    # exit   
    def __onCancelAndExit(self):
        if self.ftp is not None: self.ftp.close()
        self.__appendTextInFtpMsgBrower('Bye~~')
        if self.logFile is not None: self.logFile.close()
        app = QApplication.instance()
        app.quit()

    # 檢查地端目錄是否存在，不存在則console error
    def __ensureLocalDir(self,dir):
        if os.path.isdir(dir):
            return dir
        else:
            self.__appendTextInFtpMsgBrower(f'*error* \'Upload file dir not found\'')
            return None
    # 確定遠端路徑存在，不存在則新增
    def __ensureRemoteDir(self,path):
        try:
            self.ftp.cwd(path)
        except:
            self.__appendTextInFtpMsgBrower('----- Create reomte path -----')
            self.ftp.mkd(path)
            self.ftp.cwd(path)

    # FTP 連線
    def __ftpConnect(self,host,username,password):
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(host,21)
        try:
            ftp.login(username,password)
        except error_perm:
            ftp.quit()
            raise('Username or password wrong!')
        return ftp
    
    # ftp上傳檔案
    def __uploadFile(self,localpath):
        try:
            bufsize = 1024
            remoteFilename = os.path.basename(localpath)
            with open(localpath, 'rb') as f:
                self.ftp.storbinary(f"STOR {remoteFilename}", f, bufsize)
        except:
            self.__appendTextInFtpMsgBrower(f'*error* \'Upload file error\'')

    # 監聽者function綁定 tip: checkout lib/ftplib.py, line 687, in sendMessage, more info please checkout lib/__init__.py
    def __bindFtpMessageListener(self):
        pub.subscribe(self.__ftpMessageListen, 'sendMsg')
    # 監聽者function    
    def __ftpMessageListen(self,msg):
        self.__appendTextInFtpMsgBrower(msg)

    # 紀錄形式，如果是autoupload mode則寫入log file，否則顯示於message box
    def __appendTextInFtpMsgBrower(self,text):
        if self.autoUpload == True:
            self.logFile.write(f'{text}\n')
        else:
            self.ftpMessageBrowser.append(text)
    
    # rstrip FormData
    def __rstripFormData(self):
        self.ftpHostInput.setText(self.ftpHostInput.text().rstrip())
        self.ftpPathInput.setText(self.ftpPathInput.text().rstrip())
        self.ftpAccountInput.setText(self.ftpAccountInput.text().rstrip())
        self.ftpPasswordInput.setText(self.ftpPasswordInput.text().rstrip())
    
    # valid FormData
    def __validFormData(self):
        if self.ftpHostInput.text() == '':
            self.__appendTextInFtpMsgBrower('Error : FTP Host 不可為空')
            return False
        if self.ftpPathInput.text() == '':
            self.__appendTextInFtpMsgBrower('Error : FTP Path 不可為空')
            return False
        if self.ftpAccountInput.text() == '':
            self.__appendTextInFtpMsgBrower('Error : FTP Account 不可為空')
            return False
        if self.ftpPasswordInput.text() == '':
            self.__appendTextInFtpMsgBrower('Error : FTP Password 不可為空')
            return False
        return True
        
