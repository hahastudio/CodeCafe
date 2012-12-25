# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Client.ui'
#
# Created: Tue Dec 25 20:01:53 2012
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
        MainWindow.resize(757, 489)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 611, 441))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.Tab1 = QtGui.QWidget()
        self.Tab1.setObjectName(_fromUtf8("Tab1"))
        self.Board = TextEdit(self.Tab1)
        self.Board.setGeometry(QtCore.QRect(10, 30, 331, 381))
        self.Board.setObjectName(_fromUtf8("Board"))
        self.appointment = TextEdit(self.Tab1)
        self.appointment.setGeometry(QtCore.QRect(350, 210, 241, 201))
        self.appointment.setObjectName(_fromUtf8("appointment"))
        self.calendarWidget = QtGui.QCalendarWidget(self.Tab1)
        self.calendarWidget.setGeometry(QtCore.QRect(350, 10, 248, 169))
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.label = QtGui.QLabel(self.Tab1)
        self.label.setGeometry(QtCore.QRect(10, 10, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.Tab1)
        self.label_2.setGeometry(QtCore.QRect(350, 190, 81, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tabWidget.addTab(self.Tab1, _fromUtf8(""))
        self.Tab2 = QtGui.QWidget()
        self.Tab2.setObjectName(_fromUtf8("Tab2"))
        self.ChatBrowser = QtGui.QTextBrowser(self.Tab2)
        self.ChatBrowser.setGeometry(QtCore.QRect(10, 0, 581, 271))
        self.ChatBrowser.setObjectName(_fromUtf8("ChatBrowser"))
        self.ChatEdit = QtGui.QTextEdit(self.Tab2)
        self.ChatEdit.setGeometry(QtCore.QRect(110, 300, 481, 91))
        self.ChatEdit.setObjectName(_fromUtf8("ChatEdit"))
        self.sendButton = QtGui.QPushButton(self.Tab2)
        self.sendButton.setGeometry(QtCore.QRect(490, 390, 89, 23))
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.label_4 = QtGui.QLabel(self.Tab2)
        self.label_4.setGeometry(QtCore.QRect(10, 280, 54, 12))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.Tab2)
        self.label_5.setGeometry(QtCore.QRect(110, 280, 54, 12))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.toEdit = QtGui.QTextEdit(self.Tab2)
        self.toEdit.setGeometry(QtCore.QRect(10, 300, 91, 91))
        self.toEdit.setObjectName(_fromUtf8("textEdit"))
        self.tabWidget.addTab(self.Tab2, _fromUtf8(""))
        self.Tab3 = QtGui.QWidget()
        self.Tab3.setObjectName(_fromUtf8("Tab3"))
        self.uploadButton = QtGui.QPushButton(self.Tab3)
        self.uploadButton.setGeometry(QtCore.QRect(510, 120, 75, 23))
        self.uploadButton.setObjectName(_fromUtf8("uploadButton"))
        self.FileList = QtGui.QTreeWidget(self.Tab3)
        self.FileList.setGeometry(QtCore.QRect(0, 170, 591, 211))
        self.FileList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.FileList.setObjectName(_fromUtf8("FileList"))
        self.FileList.headerItem().setText(0, _fromUtf8("Filename"))
        self.deleteButton = QtGui.QPushButton(self.Tab3)
        self.deleteButton.setGeometry(QtCore.QRect(510, 390, 75, 23))
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.downloadButton = QtGui.QPushButton(self.Tab3)
        self.downloadButton.setGeometry(QtCore.QRect(420, 390, 75, 23))
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.uploadList = QtGui.QListWidget(self.Tab3)
        self.uploadList.setGeometry(QtCore.QRect(0, 0, 501, 141))
        self.uploadList.setObjectName(_fromUtf8("uploadList"))
        self.label_6 = QtGui.QLabel(self.Tab3)
        self.label_6.setGeometry(QtCore.QRect(510, 10, 54, 12))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.Tab3)
        self.label_7.setGeometry(QtCore.QRect(0, 150, 101, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.tabWidget.addTab(self.Tab3, _fromUtf8(""))
        self.NameList = QtGui.QListWidget(self.centralwidget)
        self.NameList.setGeometry(QtCore.QRect(620, 30, 131, 411))
        self.NameList.setObjectName(_fromUtf8("NameList"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(620, 10, 81, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 757, 23))
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
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Board", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Appointments", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), QtGui.QApplication.translate("MainWindow", "Board", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("MainWindow", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "To", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Message", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), QtGui.QApplication.translate("MainWindow", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadButton.setText(QtGui.QApplication.translate("MainWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.FileList.setSortingEnabled(True)
        self.FileList.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Date(Changes)", None, QtGui.QApplication.UnicodeUTF8))
        self.FileList.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Owner", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("MainWindow", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "To Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Files on Server", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab3), QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Online Users:", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogin.setText(QtGui.QApplication.translate("MainWindow", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setText(QtGui.QApplication.translate("MainWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setToolTip(QtGui.QApplication.translate("MainWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetPwd.setText(QtGui.QApplication.translate("MainWindow", "Set Password", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetPath.setText(QtGui.QApplication.translate("MainWindow", "Set Path", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))

