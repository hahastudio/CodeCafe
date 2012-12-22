# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Path.ui'
#
# Created: Fri Dec 21 10:28:48 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Path(object):
    def setupUi(self, PathDlg):
        PathDlg.setObjectName(_fromUtf8("PathDlg"))
        PathDlg.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(PathDlg)
        self.buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox = QtGui.QGroupBox(PathDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 381, 51))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.pathEdit = QtGui.QLineEdit(self.groupBox)
        self.pathEdit.setGeometry(QtCore.QRect(10, 20, 281, 21))
        self.pathEdit.setObjectName(_fromUtf8("pathEdit"))
        self.openPathButton = QtGui.QPushButton(self.groupBox)
        self.openPathButton.setGeometry(QtCore.QRect(300, 20, 75, 23))
        self.openPathButton.setObjectName(_fromUtf8("openPathButton"))
        self.groupBox_2 = QtGui.QGroupBox(PathDlg)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 60, 381, 201))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.filePatternEdit = QtGui.QLineEdit(self.groupBox_2)
        self.filePatternEdit.setGeometry(QtCore.QRect(10, 20, 201, 21))
        self.filePatternEdit.setObjectName(_fromUtf8("filePatternEdit"))
        self.addPatternButton = QtGui.QPushButton(self.groupBox_2)
        self.addPatternButton.setGeometry(QtCore.QRect(220, 20, 75, 23))
        self.addPatternButton.setObjectName(_fromUtf8("addPatternButton"))
        self.patternList = QtGui.QListWidget(self.groupBox_2)
        self.patternList.setGeometry(QtCore.QRect(10, 50, 361, 141))
        self.patternList.setObjectName(_fromUtf8("patternList"))
        self.delPatternButton = QtGui.QPushButton(self.groupBox_2)
        self.delPatternButton.setGeometry(QtCore.QRect(300, 20, 75, 23))
        self.delPatternButton.setObjectName(_fromUtf8("delPatternButton"))

        self.retranslateUi(PathDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PathDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PathDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(PathDlg)

    def retranslateUi(self, PathDlg):
        PathDlg.setWindowTitle(QtGui.QApplication.translate("PathDlg", "Set Project Path", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PathDlg", "Project Path", None, QtGui.QApplication.UnicodeUTF8))
        self.openPathButton.setText(QtGui.QApplication.translate("PathDlg", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PathDlg", "File Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.addPatternButton.setText(QtGui.QApplication.translate("PathDlg", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.delPatternButton.setText(QtGui.QApplication.translate("PathDlg", "Delete", None, QtGui.QApplication.UnicodeUTF8))

