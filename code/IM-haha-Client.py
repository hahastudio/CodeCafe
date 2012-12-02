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
from UI_Client import Ui_Form

import sys
reload(sys)
sys.setdefaultencoding('utf-8') #中文化

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

class ClientWidget(QWidget, Ui_Form):
    """
    IM-haha的客户端的实现类，程序的主要部分。
    """
    def __init__(self, parent = None):
        """
        __init__(self, parent = None)
        初始化UI，关联按钮的信号和槽。
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.sendMsg)
        self.pushButton_3.clicked.connect(self.connectto)

    def connectto(self):
        """
        connectto(self)
        实例化Thread2，尝试与服务端进行连接。
        关联Thread1的实例self.th的信号和槽，并报告是否成功。
        """
        self.Host = self.hisIP.displayText()
        self.Port = int(self.hisport.displayText())
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = str(self.yourname.displayText()) if self.yourname.displayText() else getip()
        try:
            self.s.connect((self.Host, self.Port))
            self.th = Thread2(self.s)
            self.th.start()
            QtCore.QObject.connect(self.th, QtCore.SIGNAL("pressed()"), self.display)
            self.textBrowser.append('连接到%s : %d'.decode('utf-8') % (self.Host, self.Port))
            self.s.send("login %s\r\n" % self.name)
        except socket.error:
            self.textBrowser.append('连接%s : %d失败'.decode('utf-8') % (self.Host, self.Port))            

    def sendMsg(self):
        """
        sendMsg(self)
        用于格式化消息，并发送给服务端。
        可以不定义昵称。
        """
        txt = self.textEdit.toPlainText()
        msg = str(txt).decode('utf-8')
        self.s.send("say "+msg+"\r\n")
        self.textEdit.setText("")
        
    def display(self):
        """
        display(self)
        将聊天记录表现在textBrowser部件上。
        """
        self.textBrowser.append((self.th.message).decode('utf-8') ) 
        
if  __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlg = ClientWidget()
    dlg.show()
    sys.exit(app.exec_())

