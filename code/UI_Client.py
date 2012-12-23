# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Client.ui'
#
# Created: Fri Dec 21 10:29:00 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class TextEdit(QtGui.QTextEdit):
    """
    A TextEdit editor that sends editingFinished events 
    when the text was changed and focus is lost.
    """

    editingFinished = QtCore.pyqtSignal()
    receivedFocus = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        super(TextEdit, self).__init__(parent)
        self._changed = False
        self.setTabChangesFocus( True )
        self.textChanged.connect( self._handle_text_changed )

    def focusInEvent(self, event):
        super(TextEdit, self).focusInEvent( event )
        self.receivedFocus.emit()

    def focusOutEvent(self, event):
        if self._changed:
            self.editingFinished.emit()
        super(TextEdit, self).focusOutEvent( event )
        self._changed = False

    def _handle_text_changed(self):
        self._changed = True

    def setTextChanged(self, state=True):
        self._changed = state

    def setHtml(self, html):
        QtGui.QTextEdit.setHtml(self, html)
        self._changed = False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(740, 489)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 601, 441))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.Tab1 = QtGui.QWidget()
        self.Tab1.setObjectName(_fromUtf8("Tab1"))
        self.Board = TextEdit(self.Tab1)
        self.Board.setGeometry(QtCore.QRect(10, 10, 561, 191))
        self.Board.setObjectName(_fromUtf8("Board"))
        self.appointment1 = TextEdit(self.Tab1)
        self.appointment1.setGeometry(QtCore.QRect(10, 260, 181, 151))
        self.appointment1.setObjectName(_fromUtf8("appointment1"))
        self.appointment2 = TextEdit(self.Tab1)
        self.appointment2.setGeometry(QtCore.QRect(200, 260, 181, 151))
        self.appointment2.setObjectName(_fromUtf8("appointment2"))
        self.appointment3 = TextEdit(self.Tab1)
        self.appointment3.setGeometry(QtCore.QRect(390, 260, 181, 151))
        self.appointment3.setObjectName(_fromUtf8("appointment3"))
        self.tabWidget.addTab(self.Tab1, _fromUtf8(""))
        self.Tab2 = QtGui.QWidget()
        self.Tab2.setObjectName(_fromUtf8("Tab2"))
        self.ChatBrowser = QtGui.QTextBrowser(self.Tab2)
        self.ChatBrowser.setGeometry(QtCore.QRect(10, 0, 571, 281))
        self.ChatBrowser.setObjectName(_fromUtf8("ChatBrowser"))
        self.ChatEdit = QtGui.QTextEdit(self.Tab2)
        self.ChatEdit.setGeometry(QtCore.QRect(10, 290, 571, 101))
        self.ChatEdit.setObjectName(_fromUtf8("ChatEdit"))
        self.sendButton = QtGui.QPushButton(self.Tab2)
        self.sendButton.setGeometry(QtCore.QRect(490, 390, 89, 23))
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.tabWidget.addTab(self.Tab2, _fromUtf8(""))
        self.Tab3 = QtGui.QWidget()
        self.Tab3.setObjectName(_fromUtf8("Tab3"))
        self.uploadButton = QtGui.QPushButton(self.Tab3)
        self.uploadButton.setGeometry(QtCore.QRect(510, 120, 75, 23))
        self.uploadButton.setObjectName(_fromUtf8("uploadButton"))
        self.FileList = QtGui.QListWidget(self.Tab3)
        self.FileList.setGeometry(QtCore.QRect(0, 150, 591, 231))
        self.FileList.setObjectName(_fromUtf8("FileList"))
        self.deleteButton = QtGui.QPushButton(self.Tab3)
        self.deleteButton.setGeometry(QtCore.QRect(510, 390, 75, 23))
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.downloadButton = QtGui.QPushButton(self.Tab3)
        self.downloadButton.setGeometry(QtCore.QRect(420, 390, 75, 23))
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.uploadList = QtGui.QListWidget(self.Tab3)
        self.uploadList.setGeometry(QtCore.QRect(0, 0, 501, 141))
        self.uploadList.setObjectName(_fromUtf8("uploadList"))
        self.tabWidget.addTab(self.Tab3, _fromUtf8(""))
        self.NameList = QtGui.QListWidget(self.centralwidget)
        self.NameList.setGeometry(QtCore.QRect(610, 20, 131, 421))
        self.NameList.setObjectName(_fromUtf8("NameList"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName(_fromUtf8("menuProject"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtGui.QAction(MainWindow)
        self.actionLogin.setObjectName(_fromUtf8("actionLogin"))
        self.actionLogout = QtGui.QAction(MainWindow)
        self.actionLogout.setObjectName(_fromUtf8("actionLogout"))
        self.actionSetPwd = QtGui.QAction(MainWindow)
        self.actionSetPwd.setObjectName(_fromUtf8("actionSetPwd"))
        self.actionSetPath = QtGui.QAction(MainWindow)
        self.actionSetPath.setObjectName(_fromUtf8("actionSetPath"))
        self.actionRefresh = QtGui.QAction(MainWindow)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.menu.addAction(self.actionLogin)
        self.menu.addAction(self.actionLogout)
        self.menu.addAction(self.actionSetPwd)
        self.menuProject.addAction(self.actionSetPath)
        self.menuProject.addAction(self.actionRefresh)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CodeCafe", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), QtGui.QApplication.translate("MainWindow", "Board", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("MainWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), QtGui.QApplication.translate("MainWindow", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadButton.setText(QtGui.QApplication.translate("MainWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("MainWindow", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab3), QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogin.setText(QtGui.QApplication.translate("MainWindow", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setText(QtGui.QApplication.translate("MainWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setToolTip(QtGui.QApplication.translate("MainWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetPwd.setText(QtGui.QApplication.translate("MainWindow", "Set Password", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetPath.setText(QtGui.QApplication.translate("MainWindow", "Set Path", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))

