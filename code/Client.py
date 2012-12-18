# -*- coding: utf-8 -*-

"""
所有导入的模块
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QLineEdit
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QTextCodec
import socket
import re
import time
from UI_Client import Ui_MainWindow
from UI_Login import Ui_Login
from threading import RLock

import sys
reload(sys)
sys.setdefaultencoding('utf-8') #中文化

MESSAGEHOST = "localhost"
MESSAGEPORT = 50000
FILEHOST = "localhost"
FILEPORT = 50001
msgLock = RLock()
msgLst = []

def getip():
    """
    getip()
    使用socket模块中的gethostbyname_ex(hostname)函数，
    返回非192开头的ipv4地址，即公网地址，因此要求服务器必须连在公网上。
    """
    names, aliases, ips = socket.gethostbyname_ex(socket.gethostname())
    for ip in ips :
        if not re.match('^192', ip):
            return ip
    return ips[0]

class Thread2(QtCore.QThread):
    """
    Qt模块下QThread的子类，用于管理socket的连接线程，使发送与接收互不干扰。
    客户端使用该线程2。
    """
    pressed = QtCore.pyqtSignal()
    def __init__(self, s):
        """
        __init__(self, s)
        初始化实例，接收服务器socket对象s，
        """
        super(Thread2, self).__init__()
        self.s = s
        #self.message = ""

    def run(self):
        """
        run(sef)
        与服务器连接，并接受消息(<=1kB)
        这里有死循环。
        """
        while 1:
            msg = self.s.recv(1024)
            if msg != "":
                #self.message = msg
                msgLock.acquire()
                msgLst.append(msg)
                msgLock.release()
                self.pressed.emit()
            #else:
                #self.message = self.message

class ClientWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        """
        __init__(self, parent = None)
        初始化UI，关联按钮的信号和槽。
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.loginDlg = QtGui.QDialog()
        self.loginDlgUI = Ui_Login()
        self.loginDlgUI.setupUi(self.loginDlg)
        #connect functions
        self.sendButton.clicked.connect(self.sendMsg)
        self.actionLogin.triggered.connect(self.openLoginDlg)
        self.actionLogout.triggered.connect(self.logout)
        self.actionRefresh.triggered.connect(self.refresh)
        self.loginDlgUI.buttonBox.accepted.connect(self.login)
        self.EditBoardButton.clicked.connect(self.editBoard)
        self.EditAppointment1Button.clicked.connect(self.editAppointment1)
        self.EditAppointment2Button.clicked.connect(self.editAppointment2)
        self.EditAppointment3Button.clicked.connect(self.editAppointment3)

        self.loginDlgUI.paswordEdit.setEchoMode(QLineEdit.Password)

        self.MessageHost = MESSAGEHOST
        self.MessagePort = MESSAGEPORT
        self.FileHost = FILEHOST
        self.FilePort = FILEPORT
        self.username = None
        self.password = None
        self.MessageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.MessageSocket.connect((self.MessageHost, self.MessagePort))
            self.th = Thread2(self.MessageSocket)
            self.th.start()
            QtCore.QObject.connect(self.th, QtCore.SIGNAL("pressed()"), self.display)
            self.ChatBrowser.append('连接到%s : %d'.decode('utf-8') % (self.MessageHost, self.MessagePort))
        except socket.error:
            self.ChatBrowser.append('连接%s : %d失败'.decode('utf-8') % (self.MessageHost, self.MessagePort))

    def openLoginDlg(self):
        self.loginDlg.show()

    def login(self):
        self.username = str(self.loginDlgUI.usernameEdit.text())
        self.password = str(self.loginDlgUI.paswordEdit.text())
        self.MessageSocket.sendall("login %s %s\r\n" % (self.username, self.password))
        self.loginDlgUI.usernameEdit.setText("")
        self.loginDlgUI.paswordEdit.setText("")
        self.loginDlg.close()
        self.refresh()

    def logout(self):
        self.MessageSocket.sendall("logout\r\n")

    def display(self):
        global msgLst
        msgLock.acquire()
        msgs = ("".join(m for m in msgLst).decode("utf-8")).split("\r\n")
        msgLst = []
        msgLock.release()
        #msgs = self.th.message.decode('utf-8').split("\r\n")
        for msg in msgs:
            if msg.startswith("board"):
                cmd, content = msg.split(' ', 1)
                self.Board.setText(content)
            elif msg.startswith("appointment"):
                cmd, index, appt = msg.split(' ', 2)
                if index == '0':
                    self.appointment1.setText(appt)
                elif index == '1':
                    self.appointment2.setText(appt)
                elif index == '2':
                    self.appointment3.setText(appt)
            elif msg.startswith("user"):
                userList = msg.split(' ')[1:]
                self.NameList.clear()
                for user in userList:
                    self.NameList.addItem(user)
            elif msg:
                self.ChatBrowser.append(msg+"\n")

    def editBoard(self):
        board = str(self.Board.toPlainText()).decode("utf-8")
        self.MessageSocket.sendall("editBoard %s\r\n" % board)

    def editAppointment1(self):
        appointment1 = str(self.appointment1.toPlainText()).decode("utf-8")
        self.MessageSocket.sendall("editAppointment 0 %s\r\n" % appointment1)

    def editAppointment2(self):
        appointment2 = str(self.appointment2.toPlainText()).decode("utf-8")
        self.MessageSocket.sendall("editAppointment 1 %s\r\n" % appointment2)

    def editAppointment3(self):
        appointment3 = str(self.appointment3.toPlainText()).decode("utf-8")
        self.MessageSocket.sendall("editAppointment 2 %s\r\n" % appointment3)

    def sendMsg(self):
        txt = self.ChatEdit.toPlainText()
        msg = str(txt).decode('utf-8')
        self.MessageSocket.sendall("say %s\r\n" % msg)
        self.ChatEdit.setText("")

    def refresh(self):
        self.MessageSocket.sendall("refresh\r\n")

    def uploadFile(self):
        pass

    def downloadFile(self):
        pass

    def deleteFile(self):
        pass

if  __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg = ClientWindow()
    dlg.show()
    sys.exit(app.exec_())