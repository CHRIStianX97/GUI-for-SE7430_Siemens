# @Date    : 2019-07-09
# @Author  : James(Jiaxing) Yang
# @File	   : AnGui.py
# @Version : $0.3$

# @Date    : 2021-01-13
# @Editer  : Tianzhi XIE


import serial
import time
import re


#different channels, the passed in index is a list that contains the test info
##def channel_selection(ser,indexes):
##    command = ""
##    #indexes is a tuple
##    for a in indexes:
##        if a == 1:
##            command += "H"
##        else:
##            command += "L"
##
##    ret_val = ser.write(command.encode())
##    if not ret_val:
##        raise ValueError("Channel selection failed")



#open the corresponding port
def port_open(portx, bbr = 9600, time = None):
    ret = False
    ser = None
    #to see any errors
    try:
        ser = serial.Serial(portx,bbr,bytesize = 8, timeout = 0)
        if (ser.is_open):
            ret = True

    except Exception:
        print("Exception happened")
        ret = False

    #to see whether or not it opened successfully
    return ret, ser

##def ACW_basic(ser,filename,index):
##    #create a test file
##    file = "FN "+ str(index) + "," + filename + "\n"
##
##    #print(file)
##    ret_val = ser.write(file.encode())
##    if ret_val:
##        return True
##    return False


#specified the test data
def ACW_test(voltage, uplimit, downlimit,testtime,channel,ser):

    ser.write("FN 1,TempTest\n".encode())
    #command transition needs time
    time.sleep(0.1)

    ret_val = ser.write("SAA\n".encode())
    time.sleep(0.1)

    if not ret_val:
        raise ValueError("SAA transimission failed")

    dw_cmd = "EV " + str(voltage)+"\n"
    ser.write(dw_cmd.encode())
    time.sleep(0.1)

    dw_cmd = "EHT " + str(uplimit)+"\n"
    ser.write(dw_cmd.encode())
    time.sleep(0.1)

    dw_cmd = "ELT " + str(downlimit)+"\n"
    ser.write(dw_cmd.encode())
    time.sleep(0.1)

    dw_cmd = "ERU "+"2\n"
    ser.write(dw_cmd.encode())
    time.sleep(0.1)

    dw_cmd = "EDW " + str(testtime)+"\n"
    ser.write(dw_cmd.encode())
    time.sleep(0.1)

    dw_cmd = "ERD " + "2\n"
    ser.write(dw_cmd.encode())
    time.sleep(0.1)

    dw_cmd = "ES " + str(channel) + "OOOOOOOO\n"
    ser.write(dw_cmd.encode())
    time.sleep(0.1)

def get_test_result(ser,dw_time):

    time.sleep(dw_time)
    search_cmd = "TD?\n"
    ret_val = ser.write(search_cmd.encode())
    time.sleep(0.1)
    str = ""
    index = 0
    while True:
        if ser.in_waiting and index < 30:
            time.sleep(2)
            str = ser.read(ser.in_waiting).decode()
            if (str == "exit"):
                break
            else:
                pass
        else:
            break

    filter = re.search(r'[\w]+[,][\w]+[,][^\t\n]+[,][\w|\.]+[,][\w|\.]+[,][\w|\.]+[,][\w|\.]+',str)
    str = filter.group()
    ser.write(("RESET\n").encode())
    time.sleep(0.1)
    return str


#make sure the analyzer's mode is single step mode
def single_step(ser):
    time.sleep(0.15)
    single_cmd = "SSI 1\n"
    ret_val = ser.write(single_cmd.encode())
    time.sleep(0.1)
    #print(ret_val.decode())
    return

#determine the communication status
def check_status(ser):
    index = 0
    str = None
    ret_val = ser.write("*TST?\n".encode())
    time.sleep(0.1)
    if not ret_val:
        raise ValueError("SAA transimission failed")
    while True:
        index += 1
        if ser.in_waiting and index <= 200:
            time.sleep(2)
            str = ser.read(ser.in_waiting).decode()
            if (str == "exit"):
                break
            else:
                print("data:", str)
                if str:
                    return True
            index += 1
        else:
            break


    return False

##if __name__ == "__main__":
##    #test example
##    ret,ser = port_open("COM8")
##    if not ret:
##        raise ValueError("failed to open")
##
##    flag = ACW_basic(ser, "BBBB", 1)
##    if not flag:
##        raise ValueError("failed to establish testfile")
##    single_step(ser)
##    ACW_test(2500,1, 10,ser)
##    ehi_cmd = "TEST\n"
##    ret_val = ser.write(ehi_cmd.encode())
##    if not ret_val:
##        raise ValueError("EHI transimission failed")
##    str = get_test_result(ser,1)

