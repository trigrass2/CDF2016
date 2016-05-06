# -*- coding: utf-8 -*-

import serial
import time

ser_arduino = serial.Serial(port = "COM7", baudrate = 9600, timeout=0) #Port à vérifier
if input == 'exit':
    ser_arduino.close()

global ser_arduino
global x,y,theta


def acquiert_from_arduino():
    try:
        l = ser_arduino.readline()
        l = l.decode()
        print(l)

    except :#ser.SerialTimeoutException:
        print('Data could not be read')

    return l

def attend_depart():

    l = acquiert_from_arduino()
    while l != "g":
        l = acquiert_from_arduino()

def maintient_cap(cap):
    if theta-cap > 5:
        ser_arduino.write('q')
    elif cap - theta > 5:
        ser_arduino.write('d')


def main():
    attend_depart()
    start = time.time()
    end = start + 90

    cap = 100
    ser_arduino.write('z')





ser.close()