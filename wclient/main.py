# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Thu Oct 11 16:47:24 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 92)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 31))
        self.label.setObjectName("label")
        self.wordcount = QtGui.QLineEdit(Form)
        self.wordcount.setGeometry(QtCore.QRect(160, 10, 141, 27))
        self.wordcount.setReadOnly(True)
        self.wordcount.setObjectName("wordcount")
        self.settings_button = QtGui.QPushButton(Form)
        self.settings_button.setGeometry(QtCore.QRect(20, 50, 281, 27))
        self.settings_button.setObjectName("settings_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Wordcount", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Current wordcount:", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_button.setText(QtGui.QApplication.translate("Form", "Settings", None, QtGui.QApplication.UnicodeUTF8))

