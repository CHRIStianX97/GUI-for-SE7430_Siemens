# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin_add.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(523, 457)
        self.Product_name = QtWidgets.QLineEdit(Form)
        self.Product_name.setGeometry(QtCore.QRect(250, 50, 161, 21))
        self.Product_name.setObjectName("Product_name")
        self.Order_num = QtWidgets.QLineEdit(Form)
        self.Order_num.setGeometry(QtCore.QRect(250, 110, 161, 21))
        self.Order_num.setObjectName("Order_num")
        self.OPS_type = QtWidgets.QLineEdit(Form)
        self.OPS_type.setGeometry(QtCore.QRect(250, 170, 161, 21))
        self.OPS_type.setObjectName("OPS_type")
        self.OPS_V = QtWidgets.QLineEdit(Form)
        self.OPS_V.setGeometry(QtCore.QRect(250, 230, 161, 21))
        self.OPS_V.setObjectName("OPS_V")
        self.OPS_DT = QtWidgets.QLineEdit(Form)
        self.OPS_DT.setGeometry(QtCore.QRect(250, 290, 161, 21))
        self.OPS_DT.setObjectName("OPS_DT")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(100, 50, 121, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(100, 110, 121, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(100, 170, 111, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(100, 230, 131, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(100, 290, 141, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(100, 350, 141, 21))
        self.label_6.setObjectName("label_6")
        self.OPS_CT = QtWidgets.QLineEdit(Form)
        self.OPS_CT.setGeometry(QtCore.QRect(250, 350, 161, 21))
        self.OPS_CT.setObjectName("OPS_CT")
        self.confirm_btn = QtWidgets.QPushButton(Form)
        self.confirm_btn.setGeometry(QtCore.QRect(194, 400, 101, 31))
        self.confirm_btn.setObjectName("confirm_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "SAP Number:"))
        self.label_2.setText(_translate("Form", "Product Name:"))
        self.label_3.setText(_translate("Form", "Operation Steps:"))
        self.label_4.setText(_translate("Form", "Operation Voltage"))
        self.label_5.setText(_translate("Form", "Operation Dwell Time:"))
        self.label_6.setText(_translate("Form", "Operation Current Limit:"))
        self.confirm_btn.setText(_translate("Form", "Confirm"))


