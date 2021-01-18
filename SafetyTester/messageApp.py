# @Date    : 2019-06-05
# @Author  : James(Jiaxing) Yang
# @File	   : workApp.py
# @Version : $0.2$



import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from message import *
import os


class messageApp(QMainWindow,Ui_Message):
    def __init__(self):
        super(messageApp,self).__init__()
        self.setupUi(self)


