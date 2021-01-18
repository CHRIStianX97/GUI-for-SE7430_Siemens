# @Date    : 2019-06-24
# @Author  : James(Jiaxing) Yang
# @File	   : adminApp.py
# @Version : $0.3$

# -*- coding:utf-8 -*-

from admin_addAPP import *
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from admin import *
import os
import pymssql
from workApp import *
from db_connect import *
from pprint import pprint




class adminApp(QMainWindow,Ui_admin_form):
    def __init__(self):
        super(adminApp, self).__init__()
        self.setupUi(self)
        self.nextBtn.clicked.connect(lambda: self.next_page())
        self.addBtn.clicked.connect(lambda: self.addProd())
        self.add_childBtn.clicked.connect(lambda: self.add_order())
        self.deleteBtn.clicked.connect(lambda : self.deleteProd())
        self.connect_db()
        self.init_trees()
        self.orderID = ""
        self.name = ""
        self.OPS_type = ""
        self.OPS_DT = ""
        self.OPS_CT = ""
        self.OPS_V = ""


    def connect_db(self):
        self.db1 = database(server="10.193.3.234", user="BSCE_TE_SCALE", pwd="Ss123456", db="BSCE_TE_SafetyTester")
        command = "SELECT * FROM dbo.Safety_TestItem ORDER by SAP_NUMBER"
        self.data = self.db1.ExecQuery(command)

    #Load the data to the admin page
    def init_trees(self):
        self.root = list()
        for x in range(0,len(self.data)):
            if self.data[x][3] not in self.root:
                root = QTreeWidgetItem(self.treeWidget)
                child1 = QTreeWidgetItem()
                root.setText(0, self.data[x][3])
                child1.setText(0, self.data[x][6])
                list_steps = self.data[x][10]
                splt = list_steps.split(",")
                child1.setText(1, splt[-1])
                child1.setText(2, splt[0])
                child1.setText(3, splt[2])
                child1.setText(4, splt[1])
                root.addChild(child1)
                self.root.append(self.data[x][3])
            else:
                child1 = QTreeWidgetItem()
                child1.setText(0, self.data[x][6])
                list_steps = self.data[x][10]
                splt = list_steps.split(",")
                child1.setText(1, splt[-1])
                child1.setText(2, splt[0])
                child1.setText(3, splt[2])
                child1.setText(4, splt[1])
                root.addChild(child1)
                self.root.append(self.data[x][3])

#set the pop-up window
    def add_info(self,same_product = False):
        self.prodInfo = addApp(adminpg=self, same_product = same_product,prodname=self.name)
        self.prodInfo.show()
        pprint(self.data)

#删除产品操作库
    def addProd(self):
        #有两种方式，第一种是添加一个产品，另外一种是添加整个系列
        #举个例子： root（总窗口）->child1(系列)->系列中的一个产品

        self.add_info()
        #print(self.treeWidget)

    def add_order(self):
        #root = self.treeWidget.currentItem()
        current = self.treeWidget.currentItem()
        if not current.parent():
            self.add_info(same_product=True)
        return

#增加产品操作库
    def deleteProd(self):
        stuff = self.treeWidget.currentItem()
        if stuff.parent():
            vol_value = stuff.data(2, 0)
            name_value = stuff.data(0,0)
            self.delete_child(name_value,vol_value)
            parent = stuff.parent()
            parent.removeChild(stuff)
        else:
            rootIndex = self.treeWidget.indexOfTopLevelItem(stuff)
            self.delete_parent(rootIndex)
            self.treeWidget.takeTopLevelItem(rootIndex)

        pprint(self.data)
        return

    #delete the parent according to the unique index
    def delete_parent(self,index):
        self.SAP_unique = list()

        #index is the when the info are unique
        for k in self.data:
            if k[3] not in self.SAP_unique:
                self.SAP_unique.append(k[3])


        for i in self.data:
            print(i)
            if i[3] == self.SAP_unique[index]:
                self.data.remove(i)

    #delete the selected child node
    def delete_child(self,name,vol):
        for i in self.data:
            if i[6] == name:
                steps = i[10]
                single_step = steps.split(",")
                vol_cmp = float(single_step[0])
                if vol_cmp == float(vol):
                    pprint(self.data)
                    self.data.remove(i)
                    pprint(self.data)

#跳转到下一个界面
    def next_page(self):
        self.close()
        self.workpg = workApp(data = self.data)
        self.workpg.show()


if __name__ == "__main__":
    first_layerApp = QApplication(sys.argv)
    first_layerForm = adminApp()

    first_layerForm.show()
    first_layerApp.exec_()