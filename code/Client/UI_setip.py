# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_setip.ui'
#
# Created: Wed Dec 26 19:34:45 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_IPset(object):
    def setupUi(self, IPset):
        IPset.setObjectName(_fromUtf8("IPset"))
        IPset.resize(181, 148)
        self.buttonBox = QtGui.QDialogButtonBox(IPset)
        self.buttonBox.setGeometry(QtCore.QRect(10, 110, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(IPset)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.msipEdit = QtGui.QLineEdit(IPset)
        self.msipEdit.setGeometry(QtCore.QRect(10, 30, 161, 20))
        self.msipEdit.setObjectName(_fromUtf8("msipEdit"))
        self.fsipEdit = QtGui.QLineEdit(IPset)
        self.fsipEdit.setGeometry(QtCore.QRect(10, 80, 161, 20))
        self.fsipEdit.setObjectName(_fromUtf8("fsipEdit"))
        self.label_2 = QtGui.QLabel(IPset)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 121, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(IPset)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), IPset.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), IPset.reject)
        QtCore.QMetaObject.connectSlotsByName(IPset)

    def retranslateUi(self, IPset):
        IPset.setWindowTitle(QtGui.QApplication.translate("IPset", "Set Servers\' IP", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IPset", "Message Server\'s IP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IPset", "File Server\'s IP", None, QtGui.QApplication.UnicodeUTF8))

