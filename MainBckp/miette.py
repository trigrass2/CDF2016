# -*- coding: utf-8 -*-

import serial
import time

ser_arduino = serial.Serial(port = "COM7", baudrate = 9600, timeout=0) #Port à vérifier
if input == 'exit':
    ser_arduino.close()

global ser_arduino
global x,y,theta

kp = 1/8
ki = 0 #Non utilisé
kd = 0 #Non utilisé

global kp, ki, kd

distance_arret = 2
tolerance_cap = 3
global distance_arret, tolerance_cap

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
    if abs(theta-cap) > tolerance_cap:
        ser_arduino.write(str(kp * (theta-cap))) #Poisitif : Positif moteur G, négatif moteur D

def temps_fini(t) :
    if t >= end :
        ser_arduino.write('s')
        return True
    else: return False

def main():
    attend_depart()
    start = time.time()
    end = start + 90
    global end


    cap = 100
    ser_arduino.write('z') #Avance
    while y < 300 - distance_arret:
        maintient_cap(cap)
        if temps_fini(time.time()):
            return

    ser_arduino.write('s') #Arrete tout
    ser_arduino.write('q') #Tourne à gauche (sur soi-même)
    while theta < 180 - tolerance_cap:
        if temps_fini(time.time()):
            return

    ser_arduino.write('s') #Arrete tout


    cap = 180 #en avant toute sur la cabine !
    ser_arduino.write('z') #Avance

    ser_arduino.write('f')# arrête les ultrason

    t1 = time.time()
    while time.time() < t1 + 3 :
        maintient_cap(cap)
        if temps_fini(time.time()):
            return

    ser_arduino.write('s') #Arrete tout
    while theta > 90 - tolerance_cap:
        ser_arduino.write('d') #Tourne à droite (sur soi-même)
        if temps_fini(time.time()):
            return

    ser_arduino.write('s') #Arrete tout

    cap = 90
    while y < 610 - distance_arret:
        maintient_cap(cap)
        if temps_fini(time.time()):
            return

    ser_arduino.write('s') #Arrete tout

    while theta > 0:
        ser_arduino.write('d')#Tourne à droite (sur soi-même)
        if temps_fini(time.time()):
            return

    ser_arduino.write('s') #Arrete tout

    cap = 0
    ser_arduino.write('r') #Recule
    t1 = time.time()
    while time.time() < t1 + 2 :
        maintient_cap(cap)
        if temps_fini(time.time()):
            return

    ser_arduino.write('s')#Arrete tout


    ser_arduino.write('u')#Remet les ultrasons en marche (quand même)




main()

ser_arduino.write('s')#Arrete tout

ser_arduino.close()