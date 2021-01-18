# @Date    : 2019-06-24
# @Author  : James(Jiaxing) Yang
# @File	   : productApp.py
# @Version : $0.1$




import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from admin_add import *
import os
from adminApp import *

class addApp(QMainWindow, Ui_Form):
    def __init__(self,adminpg,same_product = False,prodname = ""):
        super(addApp, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.parent = adminpg
        self.same_product = same_product
        self.prod_name = prodname
        if self.same_product:
            self.Product_name.setReadOnly(True)
            self.Product_name.setText(self.prod_name)
        self.confirm_btn.clicked.connect(lambda: self.confirm())

    def get_info(self):
        if self.same_product:
            self.parent.orderID = self.Order_num.text()
            self.parent.OPS_type = self.OPS_type.text()
            self.parent.OPS_V = self.OPS_V.text()
            self.parent.OPS_DT = self.OPS_DT.text()
            self.parent.OPS_CT = self.OPS_CT.text()
        else:
            self.parent.name = self.Product_name.text()
            self.parent.orderID = self.Order_num.text()
            self.parent.OPS_type = self.OPS_type.text()
            self.parent.OPS_V = self.OPS_V.text()
            self.parent.OPS_DT = self.OPS_DT.text()
            self.parent.OPS_CT = self.OPS_CT.text()



    def confirm(self):
        self.get_info()
        if not self.same_product:
            root = QTreeWidgetItem(self.parent.treeWidget)
            child1 = QTreeWidgetItem()
            root.setText(0, self.parent.name)
            child1.setText(0, self.parent.orderID)
            child1.setText(1, self.parent.OPS_type)
            child1.setText(2, self.parent.OPS_V)
            child1.setText(3, self.parent.OPS_DT)
            child1.setText(4, self.parent.OPS_CT)
            root.addChild(child1)
            list_steps = "%s,%s,%s,%s"%(self.parent.OPS_V,self.parent.OPS_CT,self.parent.OPS_DT,"1")
            new_data = (len(self.parent.data)+1,None, None, self.parent.orderID, None, self.parent.orderID, self.parent.name, None, None, None, list_steps)
            self.parent.data.append(new_data)
        else:
            root = self.parent.treeWidget.currentItem()
            child1 = QTreeWidgetItem()
            root.setText(0, self.parent.name)
            child1.setText(0, self.parent.orderID)
            child1.setText(1, self.parent.OPS_type)
            child1.setText(2, self.parent.OPS_V)
            child1.setText(3, self.parent.OPS_DT)
            child1.setText(4, self.parent.OPS_CT)
            root.addChild(child1)
            list_steps = "%s,%s,%s,%s" % (self.parent.OPS_V, self.parent.OPS_CT, self.parent.OPS_DT, "1")
            new_data = (len(self.parent.data)+1,None, None, self.parent.orderID, None, self.parent.orderID, self.parent.name, None, None, None, list_steps)
            self.parent.data.append(new_data)

        self.close()



