# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_admin_form(object):
    def setupUi(self, admin_form):
        admin_form.setObjectName("admin_form")
        admin_form.resize(1062, 777)
        self.treeWidget = QtWidgets.QTreeWidget(admin_form)
        self.treeWidget.setGeometry(QtCore.QRect(20, 160, 1021, 431))
        self.treeWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setDefaultSectionSize(150)
        self.deleteBtn = QtWidgets.QPushButton(admin_form)
        self.deleteBtn.setGeometry(QtCore.QRect(20, 90, 101, 61))
        self.deleteBtn.setObjectName("deleteBtn")
        self.addBtn = QtWidgets.QPushButton(admin_form)
        self.addBtn.setGeometry(QtCore.QRect(140, 90, 101, 61))
        self.addBtn.setObjectName("addBtn")
        self.nextBtn = QtWidgets.QPushButton(admin_form)
        self.nextBtn.setGeometry(QtCore.QRect(500, 630, 111, 51))
        self.nextBtn.setObjectName("nextBtn")
        self.add_childBtn = QtWidgets.QPushButton(admin_form)
        self.add_childBtn.setGeometry(QtCore.QRect(270, 90, 101, 61))
        self.add_childBtn.setObjectName("add_childBtn")

        self.retranslateUi(admin_form)
        QtCore.QMetaObject.connectSlotsByName(admin_form)

    def retranslateUi(self, admin_form):
        _translate = QtCore.QCoreApplication.translate
        admin_form.setWindowTitle(_translate("admin_form", "Form"))
        self.treeWidget.headerItem().setText(0, _translate("admin_form", "Product"))
        self.treeWidget.headerItem().setText(1, _translate("admin_form", "Required Steps"))
        self.treeWidget.headerItem().setText(2, _translate("admin_form", "Operation Voltage(V)"))
        self.treeWidget.headerItem().setText(3, _translate("admin_form", "Operation dwell time(s)"))
        self.treeWidget.headerItem().setText(4, _translate("admin_form", "Operation current limit(mA)"))
        self.deleteBtn.setText(_translate("admin_form", "删除"))
        self.addBtn.setText(_translate("admin_form", "添加产品"))
        self.nextBtn.setText(_translate("admin_form", "下一步"))
        self.add_childBtn.setText(_translate("admin_form", "添加订单号"))


