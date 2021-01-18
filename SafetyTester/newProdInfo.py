# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newProdInfo.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newProdInfo(object):
    def setupUi(self, newProdInfo):
        newProdInfo.setObjectName("newProdInfo")
        newProdInfo.resize(622, 228)
        self.label = QtWidgets.QLabel(newProdInfo)
        self.label.setGeometry(QtCore.QRect(30, 80, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.confirmBtn = QtWidgets.QPushButton(newProdInfo)
        self.confirmBtn.setGeometry(QtCore.QRect(240, 150, 141, 41))
        self.confirmBtn.setObjectName("confirmBtn")
        self.seriesNum = QtWidgets.QLineEdit(newProdInfo)
        self.seriesNum.setGeometry(QtCore.QRect(120, 80, 421, 41))
        self.seriesNum.setObjectName("seriesNum")

        self.retranslateUi(newProdInfo)
        QtCore.QMetaObject.connectSlotsByName(newProdInfo)

    def retranslateUi(self, newProdInfo):
        _translate = QtCore.QCoreApplication.translate
        newProdInfo.setWindowTitle(_translate("newProdInfo", "Form"))
        self.label.setText(_translate("newProdInfo", "序列号："))
        self.confirmBtn.setText(_translate("newProdInfo", "确认"))


