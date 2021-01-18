# @Date    : 2019-06-203
# @Author  : James(Jiaxing) Yang
# @File	   : productApp.py
# @Version : $0.1$




import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from login import *
from Prod_info import *
from testingpageApp import *

from testingpageApp import testingpageApp
import os


class prodApp(QMainWindow, Ui_Prodinfo):
    def __init__(self,prodID = "", prodNum = "", SAPno = "", user = "",com_num = "/dev/ttyUSB0",data = None):
        super(prodApp,self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.prodID = prodID
        self.prodNum = prodNum
        self.SAPno = SAPno
        self.com = com_num
        self.user = user
        self.info_state()
        self.confirmBtn.clicked.connect(lambda: self.confirm())
        self.data = data

    #初始化的内容
    def info_state(self):
        self.ProductName.setText(self.prodID)
        self.OPSsteps.setText(self.prodNum)
        self.SAP.setText(str(self.SAPno))
        self.Operator.setText(self.user)
        self.com_num.setText(self.com)

    #get the ID entered and get the info from DB
    def get_info(self):
        self.prodID = self.ProductName.text()
        self.prodNum = self.OPSsteps.text()
        self.SAPno = self.SAP.text()
        self.user = self.Operator.text()
        self.com = self.com_num.text()

    def confirm(self):
        #pass 产品ID 和数量给下一界面
        self.get_info()
        #然后切换页面
        self.close()
        self.testpg = testingpageApp(self.prodID, self.prodNum,self.SAPno,self.user,self.data,self.com)
        self.testpg.show()


if __name__ == "__main__":
    first_layerApp = QApplication(sys.argv)
    first_layerForm = prodApp()

    first_layerForm.show()
    first_layerApp.exec_()


