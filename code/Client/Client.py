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
from rsa import RSA

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QLineEdit
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QTextCodec

from UI_Client import Ui_MainWindow
from UI_Login import Ui_Login
from UI_Pwd import Ui_Pwd
from UI_Path import Ui_Path
from UI_setip import Ui_IPset

import sys
reload(sys)
sys.setdefaultencoding('utf-8') #中文化
"""
全局变量表
"""
with open("serverip.ini", "r") as inf:
    MESSAGEHOST = inf.readline().strip()
    FILEHOST = inf.readline().strip()

MESSAGEPORT = 50000
FILEPORT = 50001
SALT = "salt"
msgLock = RLock()
msgLst = []
fqueLock = RLock()
fque = deque()
fthLst = []
f2upLock = RLock()
f2upload = []
finfoLock = RLock()
finfo = []
with open("fileUploaded", "rb") as inf:
    fDict = cPickle.load(inf)

def all_files(pattern, search_path, pathsep=os.pathsep):
    """
    按指定的模式pattern和搜索路径search_path寻找文件
    """
    for path in search_path.split(pathsep):
        for match in glob.glob(os.path.join(path, pattern)):
            yield match

def writeFileUploaded(dic):
    """
    将已上传的文件写入记录中
    """
    ouf = open("fileUploaded", "wb")
    cPickle.dump(dic, ouf, 2)
    ouf.close()

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

class ThreadFile2Upload(QtCore.QThread):
    """
    用于按某一时间周期检查待上传文件的线程
    """
    def __init__(self, fileList, path, patterns):
        super(ThreadFile2Upload, self).__init__()
        self.fileList = fileList
        self.path = path
        self.patterns = patterns
        self.runable = True
    def run(self):
        while self.runable:
            fSet = set([])
            for pattern in self.patterns:
                for f in all_files(pattern, self.path):
                    fSet.add(f)
            self.fileList.clear()
            for f in fSet:
                try:
                    if os.path.getmtime(f) > fDict[f]:
                        with f2upLock:
                            f2upload.append(f)
                            self.fileList.addItem(os.path.split(f)[1].decode("utf-8"))
                except KeyError:
                    with f2upLock:
                        f2upload.append(f)
                        self.fileList.addItem(os.path.split(f)[1].decode("utf-8"))
            time.sleep(15)

class ThreadRefresh(QtCore.QThread):
    """
    用于按某一时间周期向消息服务器请求刷新的线程
    """
    def __init__(self, s):
        super(ThreadRefresh, self).__init__()
        self.s = s
        self.runable = True
        
    def run(self):
        while self.runable:
            self.s.sendall("refresh\r\n")
            time.sleep(10)

class ThreadFileRefresh(QtCore.QThread):
    """
    用于向文件服务器请求文件列表的线程
    """
    refreshed = QtCore.pyqtSignal()

    def __init__(self, fcode):
        super(ThreadFileRefresh, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fcode = fcode

    def run(self):
        global finfo
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
                with finfoLock:
                    finfo = cPickle.loads(m)
        elif m.startswith("error"):
            with msgLock:
                msgLst.append(m)
        self.refreshed.emit()
        self.s.close()

class ThreadFileUpload(QtCore.QThread):
    """
    用于向文件服务器上传文件的线程
    """
    finished = QtCore.pyqtSignal()

    def __init__(self, fcode, files, username):
        super(ThreadFileUpload, self).__init__()
        self.fcode = fcode
        self.files = files
        self.username = username

    def run(self):
        for f in self.files:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((FILEHOST, FILEPORT))
            self.s.sendall("fileaccess %s\r\n" % self.fcode)
            m = ""
            while not m:
                m = self.s.recv(1024)
            if m.startswith("info"):
                self.s.sendall("upload %s %s\r\n" % (os.path.split(f)[1], self.username))
                upf = open(f, "rb")
                while True:                       
                    data = upf.read(1024)                                         
                    if not data:   
                        break  
                    while len(data) > 0:   
                        intSent = self.s.send(data)   
                        data = data[intSent:]
                upf.close()
            elif m.startswith("error"):
                with msgLock:
                    msgLst.append(m)
            self.s.close()
            time.sleep(2)
        self.finished.emit()

class ThreadFileDownload(QtCore.QThread):
    """
    用于向文件服务器下载文件的线程
    """
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
                dwf = open(self.path+"\\"+self.filename, 'wb')
                while True:                           
                    receivedData = self.s.recv(1024)                                                           
                    if (not receivedData) or receivedData == "EOF\r\n":
                        break
                    dwf.write(receivedData)                          
                dwf.close()
        elif m.startswith("error"):
            with msgLock:
                msgLst.append(m)
        self.s.close()

class ThreadFileDelete(QtCore.QThread):
    """
    用于向文件服务器请求删除文件的线程
    """
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
            elif m.startswith("error"):
                with msgLock:
                    msgLst.append(m)
        elif m.startswith("error"):
            with msgLock:
                msgLst.append(m)
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
        self.ipDlg = QtGui.QDialog()
        self.ipDlgUI = Ui_IPset()
        self.ipDlgUI.setupUi(self.ipDlg)

        #connect functions
        self.sendButton.clicked.connect(self.sendMsg)
        self.actionLogin.triggered.connect(self.openLoginDlg)
        self.actionLogout.triggered.connect(self.logout)
        self.actionRefresh.triggered.connect(self.refresh)
        self.actionSetPwd.triggered.connect(self.openPwdDlg)
        self.actionSetPath.triggered.connect(self.openPathDlg)
        self.actionSetIP.triggered.connect(self.openIPDlg)
        self.Board.editingFinished.connect(self.editBoard)
        self.appointment.editingFinished.connect(self.editAppointment)
        self.uploadButton.clicked.connect(self.uploadFile)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.deleteButton.clicked.connect(self.deleteFile)

        self.loginDlgUI.buttonBox.accepted.connect(self.login)
        self.loginDlgUI.paswordEdit.setEchoMode(QLineEdit.Password)
        self.pwdDlgUI.buttonBox.accepted.connect(self.setpwd)
        self.pwdDlgUI.cPwdEdit.setEchoMode(QLineEdit.Password)
        self.pwdDlgUI.nPwdEdit.setEchoMode(QLineEdit.Password)
        self.pwdDlgUI.nPwdEdit_2.setEchoMode(QLineEdit.Password)
        self.pathDlgUI.openPathButton.clicked.connect(self.getPath)
        self.pathDlgUI.addPatternButton.clicked.connect(self.addPattern)
        self.pathDlgUI.delPatternButton.clicked.connect(self.delPattern)
        self.pathDlgUI.buttonBox.accepted.connect(self.savePathConfig)
        self.ipDlgUI.buttonBox.accepted.connect(self.setip)

        self.user = None
        self.rsa = None
        self.threfresh = None
        pathConfig = open("pathConfig", "rb")
        self.path = cPickle.load(pathConfig)
        self.patterns = cPickle.load(pathConfig)
        pathConfig.close()
        self.tempPatterns = [pattern for pattern in self.patterns]
        self.MessageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileWatcher = ThreadFile2Upload(self.uploadList, self.path, self.patterns)
        self.fileWatcher.start()

    def openLoginDlg(self):
        self.loginDlg.show()

    def openPwdDlg(self):
        self.pwdDlg.show()

    def openIPDlg(self):
        self.ipDlgUI.msipEdit.setText(MESSAGEHOST)
        self.ipDlgUI.fsipEdit.setText(FILEHOST)
        self.ipDlg.show()

    def openPathDlg(self):
        self.pathDlgUI.pathEdit.setText(self.path)
        self.pathDlgUI.patternList.clear()
        for pattern in self.patterns:
            self.pathDlgUI.patternList.addItem(pattern)
        self.pathDlg.show()

    def getPath(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                "Select Project Path", self.pathDlgUI.pathEdit.text(), options)
        if directory:
            self.pathDlgUI.pathEdit.setText(directory)

    def addPattern(self):
        pattern = str(self.pathDlgUI.filePatternEdit.text()).decode("utf-8")
        if not pattern in self.tempPatterns:
            self.tempPatterns.append(pattern)
            self.pathDlgUI.patternList.addItem(pattern)

    def delPattern(self):
        patternItem = self.pathDlgUI.patternList.takeItem(self.pathDlgUI.patternList.currentRow())
        pattern = patternItem.text()
        del patternItem
        try:
            self.tempPatterns.remove(pattern)
        except ValueError:
            pass

    def savePathConfig(self):
        self.path = str(self.pathDlgUI.pathEdit.text()).decode("utf-8")
        self.patterns = [pattern for pattern in self.tempPatterns]
        pathConfig = open("pathConfig", "wb")
        cPickle.dump(self.path, pathConfig, 2)
        cPickle.dump(self.patterns, pathConfig, 2)
        self.fileWatcher.path = self.path
        self.fileWatcher.patterns = self.patterns
        pathConfig.close()
        self.pathDlg.close()

    def setip(self):
        global MESSAGEHOST
        global FILEHOST
        MESSAGEHOST = str(self.ipDlgUI.msipEdit.text())
        FILEHOST = str(self.ipDlgUI.fsipEdit.text())
        with open("serverip.ini", "w") as ouf:
            ouf.write(MESSAGEHOST+"\n")
            ouf.write(FILEHOST+"\n")
        self.ipDlg.close()

    def login(self):
        username = str(self.loginDlgUI.usernameEdit.text())
        password = str(self.loginDlgUI.paswordEdit.text())
        m = hashlib.md5()
        m.update(password)
        m.update(SALT)
        if username and password:
            try:
                self.MessageSocket.connect((MESSAGEHOST, MESSAGEPORT))
                self.threcv = ThreadRecv(self.MessageSocket)
                self.threcv.start()
                QtCore.QObject.connect(self.threcv, QtCore.SIGNAL("pressed()"), self.display)
                self.ChatBrowser.append('连接到%s : %d'.decode('utf-8') % (MESSAGEHOST, MESSAGEPORT))
                self.MessageSocket.sendall("login %s %s\r\n" % (username, m.hexdigest()))
            except socket.error:
                self.ChatBrowser.append('连接%s : %d失败'.decode('utf-8') % (MESSAGEHOST, MESSAGEPORT))
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
        """
        将收到的消息分发
        """
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
                cmd, appt = msg.split(' ', 1)
                self.appointment.setText(appt.decode("utf-8"))
            elif msg.startswith("user"):
                userList = msg.split(' ')[1:]
                self.NameList.clear()
                for user in userList:
                    self.NameList.addItem(user)
            elif msg.startswith("account"):
                cmd, content = msg.split(' ', 1)
                self.user = cPickle.loads(content)
            elif msg.startswith("encrypt"):
                cmd, content = msg.split(' ', 1)
                self.rsa = cPickle.loads(content)
            elif msg.startswith("fcode"):
                cmd, fcode = msg.split(' ', 1)
                with fqueLock:
                    try:
                        freq = fque.popleft()
                        if freq[0] == "refresh":
                            self.fileRefreshThread = ThreadFileRefresh(fcode)
                            QtCore.QObject.connect(self.fileRefreshThread, QtCore.SIGNAL("refreshed()"), self.displayFileList)
                            self.fileRefreshThread.start()

                        elif freq[0] == "upload":
                            t = ThreadFileUpload(fcode, freq[1], freq[2])
                            QtCore.QObject.connect(t, QtCore.SIGNAL("finished()"), self.uploadList.clear)
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
            elif msg.startswith("say"):
                cmd, content = msg.split(' ', 1)
                header, enmsg = content.split('\n', 1)
                demsg = self.rsa.decrypt(cPickle.loads(enmsg))
                self.ChatBrowser.append("%s \n%s\n".decode("utf-8") % (header, demsg))
            elif msg:
                self.ChatBrowser.append(msg.decode("utf-8")+"\n")

    def displayFileList(self):
        global finfo
        fileinfos = finfo
        self.FileList.clear()
        for fileinfo in fileinfos:
            f = QtGui.QTreeWidgetItem(self.FileList)
            f.setText(0, fileinfo["filename"])
            for date in fileinfo["date"]:
                fdate = QtGui.QTreeWidgetItem(f)
                fdate.setText(0, fileinfo["filename"])
                fdate.setText(1, date)
                fdate.setText(2, fileinfo["owner"])

    def editBoard(self):
        board = str(self.Board.toPlainText()).decode("utf-8")
        if board and self.user["isAdmin"]:
            self.MessageSocket.sendall("editBoard %s\r\n" % board)

    def editAppointment(self):
        appointment = str(self.appointment.toPlainText()).decode("utf-8")
        if appointment and self.user["isAdmin"]:
            self.MessageSocket.sendall("editAppointment %s\r\n" % appointment)

    def sendMsg(self):
        toSomeone = str(self.toEdit.toPlainText()).decode("utf-8")
        msg = str(self.ChatEdit.toPlainText()).decode('utf-8')
        if msg:
            enmsg = self.rsa.encrypt(msg)
            nameList = set(toSomeone.split())
            if nameList:
                for name in nameList:
                    self.MessageSocket.sendall("say %s %s\r\n" % (name, cPickle.dumps(enmsg, 2)))
            else:
                self.MessageSocket.sendall("say %s %s\r\n" % ("-all", cPickle.dumps(enmsg, 2)))
        self.ChatEdit.setText("")

    def refresh(self):
        self.MessageSocket.sendall("refresh\r\n")
        self.MessageSocket.sendall("filerequest\r\n")
        with fqueLock:
            fque.append(("refresh", ))

    def uploadFile(self):
        global f2upload
        global fDict
        for f in f2upload:
            fDict[f] = os.path.getmtime(f)
        self.MessageSocket.sendall("filerequest\r\n")
        files = [f for f in f2upload]
        with fqueLock:
            fque.append(("upload", files, self.user["username"]))
        with f2upLock:
            f2upload = []
        writeFileUploaded(fDict)

    def downloadFile(self):
        self.MessageSocket.sendall("filerequest\r\n")
        fileItem = self.FileList.currentItem()
        filename = fileItem.text(0)
        date = fileItem.text(1)
        owner = fileItem.text(2)
        if date and owner:
            with fqueLock:
                fque.append(("download", filename, date, owner, self.path))

    def deleteFile(self):
        self.MessageSocket.sendall("filerequest\r\n")
        fileItem = self.FileList.currentItem()
        filename = fileItem.text(0)
        date = fileItem.text(1)
        owner = fileItem.text(2)
        if date and owner == self.user["username"]:
            with fqueLock:
                fque.append(("delete", self.user["username"], filename, date, owner))

if  __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg = ClientWindow()
    dlg.show()
    sys.exit(app.exec_())
