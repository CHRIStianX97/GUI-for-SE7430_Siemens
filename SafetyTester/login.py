# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login_state(object):
    def setupUi(self, Login_state):
        Login_state.setObjectName("Login_state")
        Login_state.resize(620, 488)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(Login_state.sizePolicy().hasHeightForWidth())
        Login_state.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(Login_state)
        self.label.setGeometry(QtCore.QRect(170, 170, 61, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Login_state)
        self.label_2.setGeometry(QtCore.QRect(170, 260, 71, 31))
        self.label_2.setObjectName("label_2")
        self.account = QtWidgets.QLineEdit(Login_state)
        self.account.setGeometry(QtCore.QRect(240, 170, 201, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.account.sizePolicy().hasHeightForWidth())
        self.account.setSizePolicy(sizePolicy)
        self.account.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.account.setObjectName("account")
        self.pwdtxt = QtWidgets.QLineEdit(Login_state)
        self.pwdtxt.setGeometry(QtCore.QRect(240, 260, 201, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.pwdtxt.sizePolicy().hasHeightForWidth())
        self.pwdtxt.setSizePolicy(sizePolicy)
        self.pwdtxt.setAutoFillBackground(False)
        self.pwdtxt.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.pwdtxt.setObjectName("pwdtxt")
        self.login = QtWidgets.QPushButton(Login_state)
        self.login.setGeometry(QtCore.QRect(260, 340, 91, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.login.sizePolicy().hasHeightForWidth())
        self.login.setSizePolicy(sizePolicy)
        self.login.setObjectName("login")
        self.label_3 = QtWidgets.QLabel(Login_state)
        self.label_3.setGeometry(QtCore.QRect(150, 70, 361, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Login_state)
        QtCore.QMetaObject.connectSlotsByName(Login_state)

    def retranslateUi(self, Login_state):
        _translate = QtCore.QCoreApplication.translate
        Login_state.setWindowTitle(_translate("Login_state", "SafetyTester_SE7430_1"))
        self.label.setText(_translate("Login_state", "账号："))
        self.label_2.setText(_translate("Login_state", "密码："))
        self.login.setText(_translate("Login_state", "确认"))
        self.label_3.setText(_translate("Login_state", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">安规测试仪使用</span></p></body></html>"))


