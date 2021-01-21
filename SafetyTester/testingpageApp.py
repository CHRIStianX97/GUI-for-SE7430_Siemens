# @Date    : 2019-06-04
# @Author  : James(Jiaxing) Yang
# @File	   : testingpageApp.py
# @Version : $0.2$


import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from testingpage import *
import os
from db_connect import *
from newProdInfoApp import *
from AnGui import *
from datetime import datetime
from workApp import *


class testingpageApp(QMainWindow, Ui_MainWindow):
    def __init__(self, prodID=None, prodNum=None, SAPno=None, operator=None, data = None,com = None):
        super(testingpageApp, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
        # 从前面的界面拿到东西
        self.com = com
        self.prodID = prodID
        self.prodNum = prodNum
        self.SAPno = SAPno
        self.operator = operator
        self.data = data
        #the steps in the table that are tested
        self.steps_tested = 0
        #communication status
        self.communication_status_flag = self.get_communication_status()

        #init some numbers
        self.hint = 0
        self.tested = 0
        self.passed = 0
        self.failed = 0
        self.testing_status = "未开始"
        self.process_flag = 0
        self.testing_status_flag = False
        self.basicinfo()
        self.testing_status_list = [0] * 30
        self.prod_step_number = 0
        self.orderinfo()
        self.operatorinfo()

        # table number should not be bigger than 10
        self.table_item_no = 0
        self.process_index = 0
        self.product_table()


        #the testing hint
        self.test_hint()

        #status bar
        self.test_progress()

        # start btn function
        self.startBtn.clicked.connect(lambda: (self.status_update(1),self.start()))
        self.resetBtn.clicked.connect(lambda: self.reset())
        #end btn function
        self.ceaseBtn.clicked.connect(lambda: self.exit())

        self.startBtn.setFocus()

        # real life time
        timer = QTimer(self)
        timer.timeout.connect(self.current_time)
        timer.start()

    def check_status(self):
        ret, ser = port_open(self.com)
        if not ret:
            raise ValueError("port打开失败")
        #flag = ACW_basic(ser, "BBBB", 1)
        #if not flag:
            #raise ValueError("建立Testcase失败")
        single_step(ser)
        ACW_test(100,10,0,2,'OOOO',ser)
        ehi_cmd = "TEST\n"
        ret_val = ser.write(ehi_cmd.encode())
        time.sleep(0.1)
        if not ret_val:
            raise ValueError("EHI transimission failed")
        try:
            result = get_test_result(ser, dw_time=float(2))
            return True
        except:
            return False

    def get_communication_status(self):
        ret = self.check_status()
        if ret:
            self.communication_status.setText("串口通讯正常")
            self.communication_status.setStyleSheet("color: green")
            self.communication_status.setStyleSheet("background: rgb(0, 255, 0)")
            self.startBtn.setEnabled(True)
        else:
            self.communication_status.setText("串口通讯失败")
            self.communication_status.setStyleSheet("color: red")
            self.communication_status.setStyleSheet("background: red")
            self.startBtn.setEnabled(False)
        self.communication_status_flag = ret
        return ret

    def update_communication_status(self):
        if self.communication_status_flag:
            self.communication_status.setText("串口通讯正常")
            self.communication_status.setStyleSheet("color: green")
            self.communication_status.setStyleSheet("background: rgb(0, 255, 0)")
        else:
            self.communication_status.setText("串口通讯失败")
            self.communication_status.setStyleSheet("color: red")
            self.communication_status.setStyleSheet("background: red")

    #update the testing status
    def update_testing_status(self,process_flag):
        if process_flag == 1:
            self.testing_status = "进行中"
            self.testingStatus.setStyleSheet("color: black")
            self.testingStatus.setStyleSheet("background: yellow")
        elif process_flag == 2:
            if self.angui_test_status:
                self.testing_status = "通过"
                self.testingStatus.setStyleSheet("color: black")
                self.testingStatus.setStyleSheet("background: rgb(0, 255, 0)")
            else:
                self.testing_status = "失败"
                self.testingStatus.setStyleSheet("color: black")
                self.testingStatus.setStyleSheet("background: red")
        else:
            self.testing_status = "未开始"
            self.testingStatus.setStyleSheet("color: black")
        self.testingStatus.setText(str(self.testing_status))



    # update basic info
    def update_info(self):
        self.orderinfo()
        self.operatorinfo()
        self.current_time()
        #update the information based on the
        self.information = self.get_info_sap()

     # update the number of passes and the status
    def update_progress(self):
        self.testedNum.setText(str(self.tested))
        self.passedNum.setText(str(self.passed))
        self.failedNum.setText(str(self.failed))
        self.update_testing_status(self.process_flag)


    # 当前时间
    def current_time(self):
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.timeBox.setText(self.time)

    # 操作员信息
    def operatorinfo(self):
        self.User_name.setText(self.operator)

    # 基本信息
    def basicinfo(self):
        for i in self.data:
            if i[3] == self.SAPno:
                self.Product_No.setText(i[3])
                self.Product_Type.setText(i[6])
                break
        self.testedNum.setText(str(self.tested))
        self.passedNum.setText(str(self.passed))
        self.failedNum.setText(str(self.failed))
        self.update_testing_status(self.process_flag)

    # 订单信息
    def orderinfo(self):
        self.OrderID.setText(self.prodID)
        self.OrderNum.setText(self.prodNum)
        self.SAP_Num.setText(self.SAPno)

    def status_update(self,flag):
        self.process_flag = flag
        self.update_testing_status(flag)
        self.hint = flag
        self.test_hint()

    # startbtn
    def start(self):
        for i in range(0,self.table_item_no):
            self.testing_data.setItem(i, 8, QTableWidgetItem("进行中"))
            a = self.testing_data.item(i,8)
            a.setBackground(QBrush(QColor(255, 255, 0)))
            self.testing_data.setStyleSheet("color: black")
        #check whether the tested order number is over(over has to start a new one)
        self.status_update(1)
        #if we have info already, we can directly start this
        self.test_progress()
        self.prodInfo = prodApp(testpg=self)
        self.prodInfo.show()

        #after gained the information, the related instuctions will be passed into the AnGui Analyzer
        #need a function here to execute the test

    def AnGui_operate(self):


        ret, ser = port_open(self.com)
        if not ret:
            raise ValueError("port打开失败")
        # make sure it is single step
        single_step(ser)
        # Only test single step right now
        start = time.time()
        operating_flag = True
        result_list = list()
        step_list = list()
        index = 0
        for i in self.information:
            #3000,5,0.5,2,HHLLL3000OO
            steps = i[-1]
            step = steps.split(",")
            #ACW_test(voltage, uplimit, downlimit,testtime,channel,ser)
            ACW_test(step[0], step[1],step[2],step[3],step[4],ser)
            ehi_cmd = "TEST\n"
            ret_val = ser.write(ehi_cmd.encode())
            time.sleep(0.1)
            if not ret_val:
                raise ValueError("EHI transimission failed")
            result = get_test_result(ser, dw_time=float(step[2] + 2 + 2 + 0.1))
            result_list.append(result)
            step_list.append(steps)
            result_list.append(";")
            step_list.append(";")
            if "PASS" not in result and (index) < self.table_item_no:
                operating_flag = False
                self.angui_test_status = 0
                self.testing_data.setItem(index, 8, QTableWidgetItem("失败"))
                a = self.testing_data.item(index, 8)
                a.setBackground(QBrush(QColor(255, 0, 0)))
            elif "PASS" in result and (index) < self.table_item_no:
                self.angui_test_status = 1
                self.testing_data.setItem(index, 8, QTableWidgetItem("通过"))
                a = self.testing_data.item(index, 8)
                a.setBackground(QBrush(QColor(0, 255, 0)))
            index += 1


        self.steps_tested = index
        self.elapsed = time.time() - start
        self.testUsedTime.setText(str(self.elapsed))
        self.tested += 1
        if operating_flag:
            self.passed += 1
        else:
            self.failed += 1
        self.store_result(result_list, step_list)
        self.status_update(2)
        # update the status bar
        self.figure_num(operating_flag)
        self.test_progress()
        # update the number etc
        self.update_progress()
        #update the other status

        self.prodInfo = prodApp(testpg=self)
        self.prodInfo.show()

    def store_result(self,result,steps):
        steps = ''.join(steps)
        result = ''.join(result)
        if "PASS" in result:
            status = "PASS"
        else:
            status = "FAIL"
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_import = "insert into dbo.TestData(ORDER_ID, ORDER_NUMBER, SAP_NUMBER, OPERATOR, EXECUTION_TIME, START_DATE_TIME,PRODUCTION_STATUS, TEST_DATA,TEST_RESULT,SERIES_NUM) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(self.OrderID.text(),self.OrderNum.text(),str(self.SAPno),self.operator,str(self.elapsed),dt,status,steps,result,str(self.seriesID))
        #print(data_import)

        self.db1 = database(server="10.193.3.234", user="BSCE_TE_SCALE", pwd="Ss123456", db="BSCE_TE_SafetyTester")
        self.db1.commit_change(data_import)

        return


    #update the number of passes and number of fails
    def figure_num(self,flag):
        if flag:
            status = 1
        else:
            status = 2
        if self.tested == 31:
            index = self.tested %30
            self.testing_status_list = [0] * 30
            self.testing_status_list[0] = status
        else:
            index = self.tested % 30 -1
            self.testing_status_list[index] = status


    # 在press start之后跳出来的小框
    # 要求scan号,and will fill the corresponding values
    def scanSAP(self):
        pass

    # 终止
    def reset(self):
        #reset everystatus bar and demos
        self.status_update(0)
        self.tested = 0
        self.passed = 0
        self.failed = 0
        self.testUsedTime.setText("")
        self.testing_status_list = [0] * 30
        self.test_progress()
        self.get_communication_status()
        for i in range(0,self.steps_tested):
            self.testing_data.setItem(i, 8, QTableWidgetItem("未开始"))
        self.testing_data.clearContents()
        self.steps_tested = 0
        self.table_item_no = 0
        self.product_table()
        #sending he reset signal to the AnGui analyzer
        return

    #退出
    def exit(self):
        #Close all the ongoing process
        self.close()

    # 测试统计,0 means has not start yet, 1 means started and pass, 2 means started and failed
    def test_progress(self):
        #print(self.testing_status_list)
        #add a flag here to show the red status when a product fails
        for x in range(0,len(self.testing_status_list)):
            if self.testing_status_list[x] == 0:
                self.draw_blank(x+1)
            elif self.testing_status_list[x] == 1:
                self.draw_green(x+1)
            elif self.testing_status_list[x] == 2:
                self.draw_red(x+1)

    def draw_green(self,index):
        if index == 1:
            self.statusbox1.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 2:
            self.statusbox2.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 3:
            self.statusbox3.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 4:
            self.statusbox4.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 5:
            self.statusbox5.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 6:
            self.statusbox6.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 7:
            self.statusbox7.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 8:
            self.statusbox8.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 9:
            self.statusbox9.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 10:
            self.statusbox10.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 11:
            self.statusbox11.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 12:
            self.statusbox12.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 13:
            self.statusbox13.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 14:
            self.statusbox14.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==15:
            self.statusbox15.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 16:
            self.statusbox16.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==17:
            self.statusbox17.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==18:
            self.statusbox18.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==19:
            self.statusbox19.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 20:
            self.statusbox20.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==21:
            self.statusbox21.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==22:
            self.statusbox22.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==23:
            self.statusbox23.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==24:
            self.statusbox24.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 25:
            self.statusbox25.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index ==26:
            self.statusbox26.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 27:
            self.statusbox27.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 28:
            self.statusbox28.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 29:
            self.statusbox29.setStyleSheet(("background-color: rgb(0, 255, 0);"))

        if index == 30:
            self.statusbox30.setStyleSheet(("background-color: rgb(0, 255, 0);"))

    def draw_red(self,index):
        if index == 1:
            self.statusbox1.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 2:
            self.statusbox2.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 3:
            self.statusbox3.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 4:
            self.statusbox4.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 5:
            self.statusbox5.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 6:
            self.statusbox6.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 7:
            self.statusbox7.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 8:
            self.statusbox8.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 9:
            self.statusbox9.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 10:
            self.statusbox10.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 11:
            self.statusbox11.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 12:
            self.statusbox12.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 13:
            self.statusbox13.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 14:
            self.statusbox14.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 15:
            self.statusbox15.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 16:
            self.statusbox16.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 17:
            self.statusbox17.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 18:
            self.statusbox18.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 19:
            self.statusbox19.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 20:
            self.statusbox20.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 21:
            self.statusbox21.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 22:
            self.statusbox22.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 23:
            self.statusbox23.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 24:
            self.statusbox24.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 25:
            self.statusbox25.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 26:
            self.statusbox26.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 27:
            self.statusbox27.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 28:
            self.statusbox28.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 29:
            self.statusbox29.setStyleSheet(("background-color: rgb(255, 0, 0);"))

        if index == 30:
            self.statusbox30.setStyleSheet(("background-color: rgb(255, 0, 0);"))
    #each index is to indicate which of the status bar has to turn to red/green/blank
    def draw_blank(self,index):
        if index == 1:
            self.statusbox1.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 2:
            self.statusbox2.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 3:
            self.statusbox3.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 4:
            self.statusbox4.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 5:
            self.statusbox5.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 6:
            self.statusbox6.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 7:
            self.statusbox7.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 8:
            self.statusbox8.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 9:
            self.statusbox9.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 10:
            self.statusbox10.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 11:
            self.statusbox11.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 12:
            self.statusbox12.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 13:
            self.statusbox13.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 14:
            self.statusbox14.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 15:
            self.statusbox15.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 16:
            self.statusbox16.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 17:
            self.statusbox17.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 18:
            self.statusbox18.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 19:
            self.statusbox19.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 20:
            self.statusbox20.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 21:
            self.statusbox21.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 22:
            self.statusbox22.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 23:
            self.statusbox23.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 24:
            self.statusbox24.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 25:
            self.statusbox25.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 26:
            self.statusbox26.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 27:
            self.statusbox27.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 28:
            self.statusbox28.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 29:
            self.statusbox29.setStyleSheet(("background-color: rgb(255, 255, 255);"))

        if index == 30:
            self.statusbox30.setStyleSheet(("background-color: rgb(255, 255, 255);"))

    # test result
    def test_hint(self):
        '''
        get three different test status,a dn give the hints accordingly
        0: has not started
        1: started but not finished
        2: finished, display the result
        :return:
        '''
        if self.hint == 0:
            self.test_hints.setText("确定产品信息无误之后点击开始来进行检测")
            self.test_hints.setStyleSheet(("color: rgb(0, 0, 0);"))
            self.test_hints.setFontPointSize(40)
        elif self.hint == 1:
            self.test_hints.setText("产品正在进行检测中，如需关闭进程请先点停止然后再退出")
            self.test_hints.setStyleSheet(("color: rgb(0, 0, 255);"))
            self.test_hints.setFontPointSize(40)
        elif self.hint == 2:
            self.test_hints.setText("产品已检测完，此订单号通过%s个，失败%s个"%(str(self.passed),str(self.failed)))
            self.test_hints.setStyleSheet(("color: rgb(124, 0, 124);"))
            self.test_hints.setFontPointSize(40)



    # 产品表
    def product_table(self):
        self.information = self.get_info_sap()
        if (self.table_item_no + len(self.information)) > 10:
            self.testing_data.clearContents()
            self.table_item_no = 0
        for i in range(0, len(self.information)):
            info = self.information[i]
            steps = info[-1]
            single_step = steps.split(",")
            self.testing_data.setItem(self.table_item_no, 0, QTableWidgetItem((info[3])))
            self.testing_data.setItem(self.table_item_no, 1, QTableWidgetItem(info[-1]))
            self.testing_data.setItem(self.table_item_no, 2, QTableWidgetItem("安规测试仪测试"))
            self.testing_data.setItem(self.table_item_no, 3, QTableWidgetItem("ACW测试"))
            self.testing_data.setItem(self.table_item_no, 4, QTableWidgetItem(single_step[0]))
            self.testing_data.setItem(self.table_item_no, 5, QTableWidgetItem(single_step[3]))
            self.testing_data.setItem(self.table_item_no, 6, QTableWidgetItem(single_step[1]+' ~ '+single_step[2]))
            self.testing_data.setItem(self.table_item_no, 7, QTableWidgetItem(single_step[4]))
            self.testing_data.setItem(self.table_item_no, 8, QTableWidgetItem("未开始"))
            a = self.testing_data.item(self.table_item_no,8)
            a.setBackground(QBrush(QColor(255, 255, 255)))
            self.table_item_no += 1


    #search the sapno and get the output info
    def get_info_sap(self):
        information = list()
        for i in self.data:
            if i[3] == self.SAPno:
                information.append(i)

        return information













if __name__ == "__main__":
    first_layerApp = QApplication(sys.argv)
    first_layerForm = testingpageApp()

    first_layerForm.show()
    first_layerApp.exec_()
