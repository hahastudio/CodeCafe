# -*- coding: utf-8 -*-

"""
所有导入的模块
"""
import socket
import re
import time
from threading import RLock
import cPickle
import hashlib
import os
import glob
from collections import deque

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QLineEdit
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QTextCodec

from UI_Client import Ui_MainWindow
from UI_Login import Ui_Login
from UI_Pwd import Ui_Pwd
from UI_Path import Ui_Path

import sys
reload(sys)
sys.setdefaultencoding('utf-8') #中文化

MESSAGEHOST = "localhost"
MESSAGEPORT = 50000
FILEHOST = "localhost"
FILEPORT = 50001
SALT = "salt"
msgLock = RLock()
msgLst = []
fqueLock = RLock()
fque = deque()
fthLst = [None]

def all_files(pattern, search_path, pathsep=os.pathsep):
    for path in search_path.split(pathsep):
        for match in glob.glob(os.path.join(path, pattern)):
            yield match

class ThreadRecv(QtCore.QThread):
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
        super(ThreadRecv, self).__init__()
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
                with msgLock:
                    msgLst.append(msg)
                self.pressed.emit()
            #else:
                #self.message = self.message

class ThreadRefresh(QtCore.QThread):
    """docstring for ThreadRefresh"""
    def __init__(self, s):
        super(ThreadRefresh, self).__init__()
        self.s = s
        self.runable = True
        
    def run(self):
        while self.runable:
            self.s.sendall("refresh\r\n")
            self.s.sendall("filerequest\r\n")
            with fqueLock:
                fque.append(("refresh", ))
            time.sleep(10)

class ThreadFileRefresh(QtCore.QThread):
    """docstring for ThreadFileRefresh"""
    def __init__(self, fcode):
        super(ThreadFileRefresh, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fcode = fcode

    def run(self):
        self.s.connect((FILEHOST, FILEPORT))
        self.s.sendall("fileaccess %s\r\n" % self.fcode)
        m = ""
        while not m:
            m = self.s.recv(1024)
        if m.startswith("info"):
            self.s.sendall("refresh\r\n")
            while 1:
                m = self.s.recv(1024)
                if m.startswith("endlist"):
                    break
                print cPickle.loads(m)
        self.s.close()

class ThreadFileUpload(QtCore.QThread):
    """docstring for ThreadFileRefresh"""
    def __init__(self, fcode, f, username):
        super(ThreadFileUpload, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fcode = fcode
        self.f = f
        self.username = username

    def run(self):
        self.s.connect((FILEHOST, FILEPORT))
        self.s.sendall("fileaccess %s\r\n" % self.fcode)
        m = ""
        while not m:
            m = self.s.recv(1024)
        if m.startswith("info"):
            self.s.sendall("upload %s %s\r\n" % (os.path.split(self.f)[1], self.username))
            upf = open(self.f, "rb")
            while True:                       
                data = upf.read(1024)                                         
                if not data:   
                    break  
                while len(data) > 0:   
                    intSent = self.s.send(data)   
                    data = data[intSent:]
            upf.close()
        self.s.close()

class ThreadFileDownload(QtCore.QThread):
    """docstring for ThreadFileDownload"""
    def __init__(self, fcode, filename, date, owner, path):
        super(ThreadFileDownload, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fcode = fcode
        self.filename = filename
        self.date = date
        self.owner = owner
        self.path = path
    def run(self):
        self.s.connect((FILEHOST, FILEPORT))
        self.s.sendall("fileaccess %s\r\n" % self.fcode)
        m = ""
        while not m:
            m = self.s.recv(1024)
        if m.startswith("info"):
            self.s.sendall("download %s %s %s\r\n" % (self.filename, self.date, self.owner))
            m = ""
            while not m:
                m = self.s.recv(1024)
            if m.startswith("start"):
                dwf = open(self.path+self.filename, 'wb')
                while True:                           
                    receivedData = self.s.recv(1024)                                                           
                    if (not receivedData) or receivedData == "EOF\r\n":
                        break
                    dwf.write(receivedData)                        
                print "haha"   
                dwf.close()
        self.s.close()

class ThreadFileDelete(QtCore.QThread):
    """docstring for ThreadFileDelete"""
    def __init__(self, fcode, user, filename, date, fileowner):
        super(ThreadFileDelete, self).__init__()
        self.fcode = fcode
        self.user = user
        self.filename = filename
        self.date = date
        self.fileowner = fileowner
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        self.s.connect((FILEHOST, FILEPORT))
        self.s.sendall("fileaccess %s\r\n" % self.fcode)
        m = ""
        while not m:
            m = self.s.recv(1024)
        if m.startswith("info"):
            self.s.sendall("delete %s %s %s %s\r\n" % (self.user, self.filename, self.date, self.fileowner))
            m = ""
            while not m:
                m = self.s.recv(1024)
            if m.startswith("info"):
                pass
            else:
                print m
        self.s.close()
        

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
        self.pwdDlg = QtGui.QDialog()
        self.pwdDlgUI = Ui_Pwd()
        self.pwdDlgUI.setupUi(self.pwdDlg)
        self.pathDlg = QtGui.QDialog()
        self.pathDlgUI = Ui_Path()
        self.pathDlgUI.setupUi(self.pathDlg)

        #connect functions
        self.sendButton.clicked.connect(self.sendMsg)
        self.actionLogin.triggered.connect(self.openLoginDlg)
        self.actionLogout.triggered.connect(self.logout)
        self.actionRefresh.triggered.connect(self.refresh)
        self.actionSetPwd.triggered.connect(self.openPwdDlg)
        self.actionSetPath.triggered.connect(self.openPathDlg)
        self.Board.editingFinished.connect(self.editBoard)
        self.appointment1.editingFinished.connect(self.editAppointment1)
        self.appointment2.editingFinished.connect(self.editAppointment2)
        self.appointment3.editingFinished.connect(self.editAppointment3)
        self.uploadButton.clicked.connect(self.uploadFile)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.deleteButton.clicked.connect(self.deleteFile)

        self.loginDlgUI.buttonBox.accepted.connect(self.login)
        self.loginDlgUI.paswordEdit.setEchoMode(QLineEdit.Password)
        self.pwdDlgUI.buttonBox.accepted.connect(self.setpwd)
        self.pwdDlgUI.cPwdEdit.setEchoMode(QLineEdit.Password)
        self.pwdDlgUI.nPwdEdit.setEchoMode(QLineEdit.Password)
        self.pwdDlgUI.nPwdEdit_2.setEchoMode(QLineEdit.Password)

        self.user = None
        self.threfresh = None
        self.path = ""
        self.patterns = []
        self.MessageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.MessageSocket.connect((MESSAGEHOST, MESSAGEPORT))
            self.threcv = ThreadRecv(self.MessageSocket)
            self.threcv.start()
            QtCore.QObject.connect(self.threcv, QtCore.SIGNAL("pressed()"), self.display)
            self.ChatBrowser.append('连接到%s : %d'.decode('utf-8') % (MESSAGEHOST, MESSAGEPORT))
        except socket.error:
            self.ChatBrowser.append('连接%s : %d失败'.decode('utf-8') % (MESSAGEHOST, MESSAGEPORT))

    def openLoginDlg(self):
        self.loginDlg.show()

    def openPwdDlg(self):
        self.pwdDlg.show()

    def openPathDlg(self):
        self.pathDlg.show()

    def login(self):
        username = str(self.loginDlgUI.usernameEdit.text())
        password = str(self.loginDlgUI.paswordEdit.text())
        m = hashlib.md5()
        m.update(password)
        m.update(SALT)
        if username and password:
            try:
                self.MessageSocket.sendall("login %s %s\r\n" % (username, m.hexdigest()))
            except socket.error:
                self.MessageSocket.connect((MESSAGEHOST, MESSAGEPORT))
                self.threcv = ThreadRecv(self.MessageSocket)
                self.threcv.start()
                self.MessageSocket.sendall("login %s %s\r\n" % (username, m.hexdigest()))
        self.loginDlgUI.usernameEdit.setText("")
        self.loginDlgUI.paswordEdit.setText("")
        self.loginDlg.close()

    def logout(self):
        self.MessageSocket.sendall("logout\r\n")
        self.threfresh.runable = False

    def setpwd(self):
        cPwd = str(self.pwdDlgUI.cPwdEdit.text())
        nPwd = str(self.pwdDlgUI.nPwdEdit.text())
        nPwd_2 = str(self.pwdDlgUI.nPwdEdit_2.text())
        cMD5 = hashlib.md5()
        cMD5.update(cPwd)
        cMD5.update(SALT)
        cHex = cMD5.hexdigest()
        if cHex == self.user["password"]:
            if nPwd == nPwd_2:
                nMD5 = hashlib.md5()
                nMD5.update(nPwd)
                nMD5.update(SALT)
                nHex = nMD5.hexdigest()
                self.user["password"] = nHex
                self.MessageSocket.sendall("setpwd %s\r\n" % cPickle.dumps(self.user, 2))
                self.pwdDlg.close()
            else:
                reply = QtGui.QMessageBox.information(self, "error", "Please input same new password twice.")
        else:
            reply = QtGui.QMessageBox.information(self, "error", "Current password incorrect.")
        self.pwdDlgUI.cPwdEdit.setText("")
        self.pwdDlgUI.nPwdEdit.setText("")
        self.pwdDlgUI.nPwdEdit_2.setText("")

    def display(self):
        global msgLst
        with msgLock:
            msgs = ("".join(m for m in msgLst)).split("\r\n")
            msgLst = []
        #msgs = self.threcv.message.decode('utf-8').split("\r\n")
        for msg in msgs:
            if msg.startswith("board"):
                cmd, content = msg.split(' ', 1)
                self.Board.setText(content.decode("utf-8"))
            elif msg.startswith("appointment"):
                cmd, index, appt = msg.split(' ', 2)
                if index == '0':
                    self.appointment1.setText(appt.decode("utf-8"))
                elif index == '1':
                    self.appointment2.setText(appt.decode("utf-8"))
                elif index == '2':
                    self.appointment3.setText(appt.decode("utf-8"))
            elif msg.startswith("user"):
                userList = msg.split(' ')[1:]
                self.NameList.clear()
                for user in userList:
                    self.NameList.addItem(user)
            elif msg.startswith("account"):
                cmd, content = msg.split(' ', 1)
                self.user = cPickle.loads(content)
            elif msg.startswith("fcode"):
                cmd, fcode = msg.split(' ', 1)
                print fcode
                with fqueLock:
                    try:
                        freq = fque.popleft()
                        if freq[0] == "refresh":
                            t = ThreadFileRefresh(fcode)
                            fthLst[0] = t
                            t.start()
                        elif freq[0] == "upload":
                            t = ThreadFileUpload(fcode, freq[1], freq[2])
                            fthLst.append(t)
                            t.start()
                        elif freq[0] == "download":
                            t = ThreadFileDownload(fcode, freq[1], freq[2], freq[3], freq[4])
                            fthLst.append(t)
                            t.start()
                        elif freq[0] == "delete":
                            t = ThreadFileDelete(fcode, freq[1], freq[2], freq[3], freq[4])
                            fthLst.append(t)
                            t.start()
                    except IndexError:
                        pass
            elif msg.startswith("success"):
                cmd, content = msg.split(' ', 1)
                if content == "login":
                    self.threfresh = ThreadRefresh(self.MessageSocket)
                    self.threfresh.start()
            elif msg.startswith("error"):
                cmd, content = msg.split(' ', 1)
                reply = QtGui.QMessageBox.information(self, cmd, content)
            elif msg:
                self.ChatBrowser.append(msg.decode("utf-8")+"\n")

    def editBoard(self):
        board = str(self.Board.toPlainText()).decode("utf-8")
        if board:
            self.MessageSocket.sendall("editBoard %s\r\n" % board)

    def editAppointment1(self):
        appointment1 = str(self.appointment1.toPlainText()).decode("utf-8")
        if appointment1:
            self.MessageSocket.sendall("editAppointment 0 %s\r\n" % appointment1)

    def editAppointment2(self):
        appointment2 = str(self.appointment2.toPlainText()).decode("utf-8")
        if appointment2:
            self.MessageSocket.sendall("editAppointment 1 %s\r\n" % appointment2)

    def editAppointment3(self):
        appointment3 = str(self.appointment3.toPlainText()).decode("utf-8")
        if appointment3:
            self.MessageSocket.sendall("editAppointment 2 %s\r\n" % appointment3)

    def sendMsg(self):
        txt = self.ChatEdit.toPlainText()
        msg = str(txt).decode('utf-8')
        self.MessageSocket.sendall("say %s\r\n" % msg)
        self.ChatEdit.setText("")

    def refresh(self):
        self.MessageSocket.sendall("refresh\r\n")
        self.MessageSocket.sendall("filerequest\r\n")
        with fqueLock:
            fque.append(("refresh", ))

    def uploadFile(self):
        self.MessageSocket.sendall("filerequest\r\n")
        with fqueLock:
            fque.append(("upload", r"C:\ludashi.txt", self.user["username"]))

    def downloadFile(self):
        self.MessageSocket.sendall("filerequest\r\n")
        with fqueLock:
            fque.append(("download", "ludashi.txt", "2012-12-22", "guyuhao", self.path))

    def deleteFile(self):
        self.MessageSocket.sendall("filerequest\r\n")
        with fqueLock:
            fque.append(("delete", self.user["username"], "ludashi.txt", "2012-12-23", "guyuhao"))

if  __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg = ClientWindow()
    dlg.show()
    sys.exit(app.exec_())
