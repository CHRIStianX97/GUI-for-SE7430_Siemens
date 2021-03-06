# @Date    : 2019-06-04
# @Author  : James(Jiaxing) Yang
# @File	   : productApp.py
# @Version : $0.1$




import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from login import *
from newProdInfo import *
from testingpageApp import *
import os


class prodApp(QMainWindow, Ui_newProdInfo):
    def __init__(self,testpg, seriesNum=""):
        super(prodApp,self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.seriesID = seriesNum
        self.parent = testpg
        self.confirmBtn.clicked.connect(lambda: self.confirm())
        self.seriesNum.setFocus()


    #get the ID entered and get the info from DB
    def get_info(self):
        self.seriesID = self.seriesNum.text()

    def confirm(self):
        #pass 产品ID 和数量给下一界面
        self.get_info()
        #然后切换页面
        self.close()
        self.parent.seriesID = self.seriesID
        self.parent.IDnum.setText(self.seriesID)


        try:
            self.parent.AnGui_operate()
            self.parent.communication_status_flag = True
        except:
            self.parent.communication_status_flag = True

        self.parent.update_communication_status()

    def keyPressEvent(self, event):
        #不知道为什么这个enter比qtcore里面的enter值少一
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.parent.status_update(1)
            self.confirm()


if __name__ == "__main__":
    first_layerApp = QApplication(sys.argv)
    first_layerForm = prodApp()

    first_layerForm.show()
    first_layerApp.exec_()


