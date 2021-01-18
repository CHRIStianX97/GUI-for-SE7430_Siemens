# @Date    : 2019-06-03
# @Author  : James(Jiaxing) Yang
# @File	   : AnGuiApp.py
# @Version : $0.1$

# @Date    : 2021-01-06
# @Editor  : Tianzhi XIE



import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from login import *
from work import *
import os
from adminApp import *
from workApp import *


class LoginApp(QMainWindow, Ui_Login_state):
    def __init__(self):
        #initiallize
        super(LoginApp, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.pwdtxt.setEchoMode(QLineEdit.Password)
        #这是为了判断有没有东西输入
        self.info_collected = False
        #把按键连接起来
        self.login.clicked.connect(lambda: self.validation())

    #拿到user的信息
    def get_userinfo(self):
        self.user = self.account.text()
        self.pwd = self.pwdtxt.text()
        if len(self.pwd) != 0 and len(self.user) != 0:
            self.info_collected = True

    def keyPressEvent(self, event):
        #不知道为什么这个enter比qtcore里面的enter值少一
        #Windows下，Qt.Key_Return(字母键盘回车) + 1 == Qt.Key_Enter(数字小键盘回车)
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.validation()

    #判断是admin还是一般user
    def checkinfo(self):
        try:
            f = open('/home/pi/BSCE_TE/SafetyTester/admin.txt','r')
        except:
            raise ValueError("The admin file does not exist")

        admin = list()
        for x in f:
            x = x.rstrip("\n")
            splt = x.split(",")
            admin.append(splt[1])

        self.admin = admin
        f.close()

        if str(self.user) == admin[0] and str(self.pwd == admin[1]):
            #界面转为管理员模式
            self.adminpage()

        else:
            #界面转为操作员模式
            self.workerpage()

    #validate the info collected
    def validation(self):
        self.get_userinfo()
        if self.info_collected:
            self.checkinfo()


    #操作员界面跳转
    def workerpage(self):
        #先关闭登录界面
        self.close()
        self.workerpg = workApp()
        self.workerpg.show()


    #admin界面跳转
    def adminpage(self):
        self.close()
        self.adminpg = adminApp()
        self.adminpg.show()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    first_layerForm = LoginApp()
    first_layerForm.show()

    sys.exit(App.exec_())


