import serial
from serial import *
def com():
    ser=serial.Serial()
    i=1
    while i<10:
        name='COM'+str(i)
        ser.open
        try:
            ser.is_open
            ser = serial.Serial(name)
            ser.baudrate=38400
            print(name)
            return name
        except serial.serialutil.SerialException:
            pass
        i+=1
com()
