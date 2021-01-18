# @Date    : 2019-06-05
# @Author  : James(Jiaxing) Yang
# @File	   : workApp.py
# @Version : $0.2$



import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from work import *
import os
from productApp import *
from db_connect import *
import numpy as np
import pandas as pd
from messageApp import *


#change the way of getting the data
class workApp(QMainWindow,Ui_workpg):
    def __init__(self, data = None):
        super(workApp,self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.prodInfo = None
        self.taskTable.setStyleSheet("background:  rgb(230, 230, 230)")
        self.nextbtn.setEnabled(False)
        self.nextbtn.clicked.connect(lambda: self.next_step())
        self.seachBtn.clicked.connect(lambda: self.search())
        self.loaddb()
        self.row = 0
        self.data = data
        if not self.data:
            self.connect_db()

    #调用数据库放入表格中
    def loaddb(self):
        self.db1 = database(server="10.193.3.234", user="BSCE_TE_SCALE", pwd="Ss123456", db="BSCE_TE_SafetyTester")
        self.db1.get_info()
        self.data = self.db1.dr.get_values()

    def connect_db(self):
        self.db1 = database(server="10.193.3.234", user="BSCE_TE_SCALE", pwd="Ss123456", db="BSCE_TE_SafetyTester")
        command = "SELECT * FROM dbo.Safety_TestItem ORDER by SAP_NUMBER"
        self.data = self.db1.ExecQuery(command)

    def get_db_info(self):
        ret = list()
        self.SAPno = int(self.SAPID.text())
        #print(self.SAPno)
        for i in self.data:
            #print(i[3])
            if str(i[3]) == str(self.SAPno):
                ret.append(i)
        return ret
    #查询SAPnos,查询完毕之后要把SAPno和订单号那些传送到下一个界面
    def search(self):
        try:
            # only allows one sap number to be passed
            self.taskTable.clearContents()
            # 拿到要搜索的SAP值
            ret = self.get_db_info()
            if ret:
                self.row = 0
                for i in range(0,len(ret)):
                    self.shuxing = ret[i][6]
                    self.value = ret[i][10]
                    self.taskTable.setItem(self.row, 0, QTableWidgetItem(str(self.SAPno)))
                    self.taskTable.setItem(self.row, 1, QTableWidgetItem(self.shuxing))
                    self.taskTable.setItem(self.row, 2, QTableWidgetItem(self.value))
                    self.row += 1
                self.nextbtn.setEnabled(True)
            else:
                self.message_show()
        except:
            self.message_show()



    #message box
    def message_show(self):
        self.messagebox = messageApp()
        self.messagebox.show()


    #跳到operating界面
    def next_step(self):
        self.close()
        self.prodInfo = prodApp(data = self.data,SAPno=self.SAPno)
        self.prodInfo.switch = True
        self.prodInfo.show()




if __name__ == "__main__":
    first_layerApp = QApplication(sys.argv)
    first_layerForm = workApp()

    first_layerForm.show()
    first_layerApp.exec_()