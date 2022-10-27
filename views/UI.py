from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextBrowser,  QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from views.components.topLeftRightFileListWidget import TopLeftRightFileListWidget
from PyQt5 import QtCore

class Main_Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('FTP brower')
        self.resize(650, 500)

        # 第一行按钮布局管理
        self.hLayout1 = QVBoxLayout()
        # 第二行按钮布局管理
        self.hLayout2 = QVBoxLayout()

        # 建構 form
        self.formGroupBox = QGroupBox("FTP input")
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
        self.ftpPasswordInput.setEchoMode(QLineEdit.Password)
        self.formInLine.addRow(self.ftpPasswordLabel, self.ftpPasswordInput)
        self.formGroupBox.setLayout(self.formInLine)
        # 掛載form
        self.hLayout1.addWidget(self.formGroupBox)

        #創建並掛載ftpMessageBrowser
        self.ftpMessageBrowserLabel = QLabel('FTP message')
        self.ftpMessageBrowser = QTextBrowser(self)
        self.hLayout1.setSpacing(10)
        self.hLayout1.addWidget(self.ftpMessageBrowserLabel)
        self.hLayout1.addWidget(self.ftpMessageBrowser)

        # 創建並掛載DialogButtonBox
        self.DialogButtonBox = QDialogButtonBox(
             QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.hLayout1.addWidget(self.DialogButtonBox)

        
        # 創建並掛載filelistWidget
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