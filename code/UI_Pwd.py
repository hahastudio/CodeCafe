# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Pwd.ui'
#
# Created: Thu Dec 20 16:38:50 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(203, 195)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 160, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.cPwdEdit = QtGui.QLineEdit(Dialog)
        self.cPwdEdit.setGeometry(QtCore.QRect(10, 30, 181, 21))
        self.cPwdEdit.setObjectName(_fromUtf8("cPwdEdit"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.nPwdEdit = QtGui.QLineEdit(Dialog)
        self.nPwdEdit.setGeometry(QtCore.QRect(10, 80, 181, 21))
        self.nPwdEdit.setObjectName(_fromUtf8("nPwdEdit"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.nPwdEdit_2 = QtGui.QLineEdit(Dialog)
        self.nPwdEdit_2.setGeometry(QtCore.QRect(10, 130, 181, 20))
        self.nPwdEdit_2.setObjectName(_fromUtf8("nPwdEdit_2"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Set Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Current Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "New Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Please input again:", None, QtGui.QApplication.UnicodeUTF8))

