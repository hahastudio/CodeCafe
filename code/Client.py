# -*- coding: utf-8 -*-

"""
所有导入的模块
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QTextCodec
import socket
import re
import time
from UI_Client import Ui_MainWindow

import sys
reload(sys)
sys.setdefaultencoding('utf-8') #中文化

MESSAGEHOST = "localhost"
MESSAGEPORT = 50000
FILEHOST = "localhost"
FILEPORT = 50001

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
        self.message = ""

    def run(self):
        """
        run(sef)
        与服务器连接，并接受消息(<=1kB)
        这里有死循环。
        """
        while 1:
            msg = self.s.recv(1024)
            if msg != "":
                self.message = msg
                self.pressed.emit()
            else:
                self.message = self.message

class ClientWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        """
        __init__(self, parent = None)
        初始化UI，关联按钮的信号和槽。
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #connect functions

        self.MessageHost = MESSAGEHOST
        self.MessagePort = MESSAGEPORT
        self.FileHost = FILEHOST
        self.FilePort = FILEPORT
        self.MessageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.MessageSocket.connect((self.MessageHost, self.MessagePort))
            self.th = Thread2(self.MessageSocket)
            self.th.start()
            QtCore.QObject.connect(self.th, QtCore.SIGNAL("pressed()"), self.display)
            self.ChatBrowser.append('连接到%s : %d'.decode('utf-8') % (self.MessageHost, self.MessagePort))
        except socket.error:
            self.ChatBrowser.append('连接%s : %d失败'.decode('utf-8') % (self.MessageHost, self.MessagePort))

    def login(self):
        pass

    def logout(self):
        pass

    def display(self):
        pass

    def editBoard(self):
        pass

    def editAppointment1(self):
        pass

    def editAppointment2(self):
        pass

    def editAppointment3(self):
        pass

    def sendMsg(self):
        pass

    def refresh(self):
        pass