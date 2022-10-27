from asyncio.windows_events import NULL
import os
from time import sleep
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, QApplication, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QFileDialog
import re
from PyQt5 import QtWidgets, QtGui, QtCore
from topLeftRightFileListWidget import TopLeftRightFileListWidget
from os import listdir
from os.path import isfile, join
from ftplib import FTP,error_perm

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()
        self.__initVal()
        self.__initControl()

    def __initUi(self):
        self.setWindowTitle('FTP brower')
        self.resize(700, 300)

        # 第一行按钮布局管理
        self.hLayout1 = QVBoxLayout()

        # 建構 form
        self.formGroupBox = QGroupBox("Form layout")
        self.formInLine = QFormLayout()
        # ftpHost 行
        self.ftpHostLabel = QLabel("FTP Host :")
        self.ftpHostInput = QLineEdit()
        self.formInLine.addRow(self.ftpHostLabel, self.ftpHostInput)
        # ftpPath 行
        self.ftpPathLabel = QLabel("FTP Path :")
        self.ftpPathInput = QLineEdit()
        self.formInLine.addRow(self.ftpPathLabel, self.ftpPathInput)
        # ftpAccount 行
        self.ftpAccountLabel = QLabel("FTP Account :")
        self.ftpAccountInput = QLineEdit()
        self.formInLine.addRow(self.ftpAccountLabel, self.ftpAccountInput)
        # ftpPassword 行
        self.ftpPasswordLabel = QLabel("FTP Password :")
        self.ftpPasswordInput = QLineEdit()
        self.formInLine.addRow(self.ftpPasswordLabel, self.ftpPasswordInput)
        self.formGroupBox.setLayout(self.formInLine)
        # 掛載form
        self.hLayout1.addWidget(self.formGroupBox)

        # 建構DialogButtonBox
        self.DialogButtonBox = QDialogButtonBox(
             QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        # 掛載DialogButtonBox
        self.hLayout1.addWidget(self.DialogButtonBox)

        # 第二行按钮布局管理
        self.hLayout2 = QVBoxLayout()
        self.FileList = TopLeftRightFileListWidget()
        self.hLayout2.addWidget(self.FileList)

        self.lay = QHBoxLayout()
        self.lay.setSpacing(20)
        self.lay.addLayout(self.hLayout1)
        self.lay.addLayout(self.hLayout2)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.lay)
        self.setCentralWidget(self.mainWidget)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.ftpHostInput.setPlaceholderText(
            _translate("MainWindow", "Target Host"))
        self.ftpAccountInput.setPlaceholderText(
            _translate("MainWindow", "Account"))
        self.ftpPasswordInput.setPlaceholderText(
            _translate("MainWindow", "Password"))

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
                self.FileList.setFileName(os.path.abspath(file))

    def __initControl(self):
        self.DialogButtonBox.accepted.connect(self.startToUpload)
        self.DialogButtonBox.rejected.connect(self.onCancelAndExit)

    def startToUpload(self):
        self.__rstripFormData()
        vaildResult = self.__validFormData()
        
        if vaildResult:
            host = self.ftpHostInput.text()
            username = self.ftpAccountInput.text()
            password = self.ftpPasswordInput.text()
            path = self.ftpPathInput.text()

            ftp = self.ftpConnect(host,username,password)
            self.ftpEnsureDir(ftp,path)

            uploadFileAbsPathList = self.FileList.getFileName()
            for localPath in uploadFileAbsPathList:
                self.uploadFile(ftp,localPath)
            QMessageBox.information(self, 'Message box',  'upload complete!!!')

    def onCancelAndExit(self):
        QMessageBox.information(self, 'Message box',  'onCancelAndExit!!!')
    
    def ftpConnect(self,host,username,password):
        print('ftpConnect',host,username,password)
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(host,21)
        try:
            ftp.login(username,password)
        except error_perm:
            ftp.quit()
            exit(1)
        return ftp

    def ftpEnsureDir(self,ftp,path):
        try:
            ftp.cwd(path)
        except error_perm:
            ftp.mkd(path)
            sleep(1)
            ftp.cwd(path)

    def uploadFile(self,ftp,localpath):
        bufsize = 1024
        remoteFilename = os.path.basename(localpath)
        with open(localpath, 'rb') as f:
            self.ftp.storbinary("STOR %s"%remoteFilename, f, bufsize)
            ftp.set_debuglevel(0)

    def __rstripFormData(self):
        self.ftpHostInput.setText(self.ftpHostInput.text().rstrip())
        self.ftpPathInput.setText(self.ftpPathInput.text().rstrip())
        self.ftpAccountInput.setText(self.ftpAccountInput.text().rstrip())
        self.ftpPasswordInput.setText(self.ftpPasswordInput.text().rstrip())
        
    def __validFormData(self):
        if self.ftpHostInput.text() == '':
            QMessageBox.information(self, 'Error',  'FTP Host 不可為空')
            return False
        if self.ftpPathInput.text() == '':
            QMessageBox.information(self, 'Error',  'FTP Path 不可為空')
            return False
        if self.ftpAccountInput.text() == '':
            QMessageBox.information(self, 'Error',  'FTP Account 不可為空')
            return False
        if self.ftpPasswordInput.text() == '':
            QMessageBox.information(self, 'Error',  'FTP Password 不可為空')
            return False
        return True
        
