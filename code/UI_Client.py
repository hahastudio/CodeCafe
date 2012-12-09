# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\haha\Documents\GitHub\CodeCafe\code\UI_Client.ui'
#
# Created: Sun Dec 09 09:53:43 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(738, 489)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 0, 581, 441))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.Tab1 = QtGui.QWidget()
        self.Tab1.setObjectName(_fromUtf8("Tab1"))
        self.Board = QtGui.QTextBrowser(self.Tab1)
        self.Board.setGeometry(QtCore.QRect(10, 10, 561, 191))
        self.Board.setObjectName(_fromUtf8("Board"))
        self.appointment1 = QtGui.QTextBrowser(self.Tab1)
        self.appointment1.setGeometry(QtCore.QRect(10, 260, 181, 151))
        self.appointment1.setObjectName(_fromUtf8("appointment1"))
        self.appointment2 = QtGui.QTextBrowser(self.Tab1)
        self.appointment2.setGeometry(QtCore.QRect(200, 260, 181, 151))
        self.appointment2.setObjectName(_fromUtf8("appointment2"))
        self.appointment3 = QtGui.QTextBrowser(self.Tab1)
        self.appointment3.setGeometry(QtCore.QRect(390, 260, 181, 151))
        self.appointment3.setObjectName(_fromUtf8("appointment3"))
        self.EditBoardButton = QtGui.QPushButton(self.Tab1)
        self.EditBoardButton.setGeometry(QtCore.QRect(250, 200, 75, 23))
        self.EditBoardButton.setObjectName(_fromUtf8("EditBoardButton"))
        self.EditAppointment1Button = QtGui.QPushButton(self.Tab1)
        self.EditAppointment1Button.setGeometry(QtCore.QRect(60, 230, 75, 23))
        self.EditAppointment1Button.setObjectName(_fromUtf8("EditAppointment1Button"))
        self.EditAppointment2Button = QtGui.QPushButton(self.Tab1)
        self.EditAppointment2Button.setGeometry(QtCore.QRect(250, 230, 75, 23))
        self.EditAppointment2Button.setObjectName(_fromUtf8("EditAppointment2Button"))
        self.EditAppointment3Button = QtGui.QPushButton(self.Tab1)
        self.EditAppointment3Button.setGeometry(QtCore.QRect(440, 230, 75, 23))
        self.EditAppointment3Button.setObjectName(_fromUtf8("EditAppointment3Button"))
        self.tabWidget.addTab(self.Tab1, _fromUtf8(""))
        self.Tab2 = QtGui.QWidget()
        self.Tab2.setObjectName(_fromUtf8("Tab2"))
        self.ChatBrowser = QtGui.QTextBrowser(self.Tab2)
        self.ChatBrowser.setGeometry(QtCore.QRect(10, 0, 551, 281))
        self.ChatBrowser.setObjectName(_fromUtf8("ChatBrowser"))
        self.ChatEdit = QtGui.QTextEdit(self.Tab2)
        self.ChatEdit.setGeometry(QtCore.QRect(10, 290, 561, 101))
        self.ChatEdit.setObjectName(_fromUtf8("ChatEdit"))
        self.sendButton = QtGui.QPushButton(self.Tab2)
        self.sendButton.setGeometry(QtCore.QRect(470, 390, 89, 23))
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.tabWidget.addTab(self.Tab2, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.OpenFileButton = QtGui.QPushButton(self.tab)
        self.OpenFileButton.setGeometry(QtCore.QRect(480, 10, 75, 23))
        self.OpenFileButton.setObjectName(_fromUtf8("OpenFileButton"))
        self.pathEdit = QtGui.QLineEdit(self.tab)
        self.pathEdit.setGeometry(QtCore.QRect(10, 10, 461, 20))
        self.pathEdit.setObjectName(_fromUtf8("pathEdit"))
        self.FileList = QtGui.QListWidget(self.tab)
        self.FileList.setGeometry(QtCore.QRect(10, 40, 561, 371))
        self.FileList.setObjectName(_fromUtf8("FileList"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.NameList = QtGui.QListWidget(self.centralwidget)
        self.NameList.setGeometry(QtCore.QRect(580, 20, 151, 421))
        self.NameList.setObjectName(_fromUtf8("NameList"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 738, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CodeCafe", None, QtGui.QApplication.UnicodeUTF8))
        self.EditBoardButton.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAppointment1Button.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAppointment2Button.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAppointment3Button.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), QtGui.QApplication.translate("MainWindow", "Board", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("MainWindow", "å�‘é€�", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), QtGui.QApplication.translate("MainWindow", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenFileButton.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "è´¦æˆ·", None, QtGui.QApplication.UnicodeUTF8))
        self.action.setText(QtGui.QApplication.translate("MainWindow", "ç™»å…¥", None, QtGui.QApplication.UnicodeUTF8))
        self.action_2.setText(QtGui.QApplication.translate("MainWindow", "ç™»å‡º", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

