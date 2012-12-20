# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Client.ui'
#
# Created: Thu Dec 20 16:42:28 2012
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
        MainWindow.resize(738, 489)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 0, 581, 441))
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
        self.ChatBrowser.setGeometry(QtCore.QRect(10, 0, 561, 281))
        self.ChatBrowser.setObjectName(_fromUtf8("ChatBrowser"))
        self.ChatEdit = QtGui.QTextEdit(self.Tab2)
        self.ChatEdit.setGeometry(QtCore.QRect(10, 290, 561, 101))
        self.ChatEdit.setObjectName(_fromUtf8("ChatEdit"))
        self.sendButton = QtGui.QPushButton(self.Tab2)
        self.sendButton.setGeometry(QtCore.QRect(470, 390, 89, 23))
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.tabWidget.addTab(self.Tab2, _fromUtf8(""))
        self.Tab3 = QtGui.QWidget()
        self.Tab3.setObjectName(_fromUtf8("Tab3"))
        self.OpenFileButton = QtGui.QPushButton(self.Tab3)
        self.OpenFileButton.setGeometry(QtCore.QRect(480, 10, 75, 23))
        self.OpenFileButton.setObjectName(_fromUtf8("OpenFileButton"))
        self.pathEdit = QtGui.QLineEdit(self.Tab3)
        self.pathEdit.setGeometry(QtCore.QRect(10, 10, 461, 20))
        self.pathEdit.setObjectName(_fromUtf8("pathEdit"))
        self.FileList = QtGui.QListWidget(self.Tab3)
        self.FileList.setGeometry(QtCore.QRect(10, 40, 561, 371))
        self.FileList.setObjectName(_fromUtf8("FileList"))
        self.tabWidget.addTab(self.Tab3, _fromUtf8(""))
        self.NameList = QtGui.QListWidget(self.centralwidget)
        self.NameList.setGeometry(QtCore.QRect(590, 20, 141, 421))
        self.NameList.setObjectName(_fromUtf8("NameList"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 738, 23))
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
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CodeCafe", None, QtGui.QApplication.UnicodeUTF8))
        self.EditBoardButton.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAppointment1Button.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAppointment2Button.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.EditAppointment3Button.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), QtGui.QApplication.translate("MainWindow", "Board", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("MainWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), QtGui.QApplication.translate("MainWindow", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenFileButton.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab3), QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogin.setText(QtGui.QApplication.translate("MainWindow", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setText(QtGui.QApplication.translate("MainWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setToolTip(QtGui.QApplication.translate("MainWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetPwd.setText(QtGui.QApplication.translate("MainWindow", "Set Password", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetPath.setText(QtGui.QApplication.translate("MainWindow", "Set Path", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))

