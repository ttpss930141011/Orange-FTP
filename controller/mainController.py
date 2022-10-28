from asyncio.windows_events import NULL
import os
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox
import re
from os import listdir
from os.path import isfile, join
from lib.ftplib import FTP,error_perm
from pubsub import pub
from views.UI import Main_Window

class Window(QMainWindow,Main_Window):
    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initControl()
        self.__initFtp()
        self.__bindFtpMessageListen()
        

    def __initVal(self):
        config = open('config.txt', 'r')
        ftpHost = re.findall(
            r'[0-9]+(?:\.[0-9]+){3}',
            config.readline().split(':')[1])[0]
        _, _, ftpPath = config.readline().partition("FTP_Path:")
        _, _, ftpAccount = config.readline().partition("FTP_Account:")
        _, _, ftpPassword = config.readline().partition("FTP_Password:")

        # 自動帶入setting.txt
        self.ftpHostInput.setText(ftpHost)
        self.ftpPathInput.setText(ftpPath)
        self.ftpAccountInput.setText(ftpAccount)
        self.ftpPasswordInput.setText(ftpPassword)
        # 自動帶入file folder 內的檔案
        for file in listdir("./file"): 
            if isfile(join("./file", file)):
                # self.FileList.setFileName(absresgetter.getabsres(file))
                self.FileList.setFileName(os.path.abspath(f'file/{file}'))

    def __initControl(self):
        self.DialogButtonBox.accepted.connect(self.StartToUpload)
        self.DialogButtonBox.rejected.connect(self.__onCancelAndExit)
        
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
                self.ftp = NULL

    def StartToUpload(self):
        self.__initFtp()
        self.__rstripFormData()
        vaildResult = self.__validFormData()
        if not self.ftp: 
            self.__appendTextInFtpMsgBrower(f'*error* \'FTP initial error\'')
            return
        if vaildResult:
            path = self.ftpPathInput.text()
            self.__ftpEnsureDir(path)
            uploadFileAbsPathList = self.FileList.getFileName()
            self.__appendTextInFtpMsgBrower('----- Start to upload -----')
            for localPath in uploadFileAbsPathList:
                self.__uploadFile(localPath)
                self.__appendTextInFtpMsgBrower(f'*uploading* \'{os.path.basename(localPath)}\'')
            self.__appendTextInFtpMsgBrower('----- upload complete -----')

    def __onCancelAndExit(self):
        if not self.ftp: self.ftp.close()
        self.__appendTextInFtpMsgBrower('Bye~~')
        app = QApplication.instance()
        app.quit()
    
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
    
    def __ftpEnsureDir(self,path):
        try:
            self.ftp.cwd(path)
        except:
            self.__appendTextInFtpMsgBrower('----- Create reomte path -----')
            self.ftp.mkd(path)
            self.ftp.cwd(path)

    def __uploadFile(self,localpath):
        bufsize = 1024
        remoteFilename = os.path.basename(localpath)
        with open(localpath, 'rb') as f:
            self.ftp.storbinary("STOR %s"%remoteFilename, f, bufsize)

    # 監聽者function綁定
    def __bindFtpMessageListen(self):
        pub.subscribe(self.__ftpMessageListen, 'sendMsg')
    # 監聽者function    
    def __ftpMessageListen(self,msg):
        self.__appendTextInFtpMsgBrower(msg)

    def __appendTextInFtpMsgBrower(self,text):
        self.ftpMessageBrowser.append(text)
    
    def __rstripFormData(self):
        self.ftpHostInput.setText(self.ftpHostInput.text().rstrip())
        self.ftpPathInput.setText(self.ftpPathInput.text().rstrip())
        self.ftpAccountInput.setText(self.ftpAccountInput.text().rstrip())
        self.ftpPasswordInput.setText(self.ftpPasswordInput.text().rstrip())
        
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
        
