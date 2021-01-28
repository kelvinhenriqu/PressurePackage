#!/usr/bin/env python
# -*- coding: utf-8 -*-
__VERSION__ = '1.4'

import time
import pigpio
import csv
from datetime import datetime
import urllib

revisao = "1.3"
Debug = 1
started = 0
Serial="21001" #Numero Serial do produto
path = "/mnt/usb_share/logs/"

now = datetime.now()
date = now.strftime("%d%m%y%H%M%S")
csvname =path + date + "-" + Serial +".csv"
checkupdate()

def getvalue(): #Comunica com I2C e retorna valores de press?o e temperatura

    pi = pigpio.pi()
    h = pi.i2c_open(1, 0x78)
    pi.i2c_write_device(h, [0xAC])
    time.sleep(0.2)
    (b, d) = pi.i2c_read_device(h, 6)
    pi.i2c_close(h)
    pi.stop()

    p1 = bin(d[1])[2:].zfill(8) #BridgeDat1
    p2 = bin(d[2])[2:].zfill(8) #BridgeDat2
    p3 = bin(d[3])[2:].zfill(8) #BridgeDat3
    t1 = bin(d[4])[2:].zfill(8) #TempDat1
    t2 = bin(d[5])[2:].zfill(8) #TempDat2
    press = p1+p2+p3
    dpress = int(press, 2)
    Pressure = (((((dpress/12305550)*100)*6)/100)-2.2)*1.042
    temp = t1+t2
    dtemp = int(temp, 2)
    Temperature = (((dtemp/65536)*190)-40)*0.954

    if Debug > 0:
        print()
        if Pressure < -1 or Pressure > 5:
            print("out of range")
        else:
            print("Pressao = ", Pressure, "bar")

        if Temperature <0 or Temperature >100:
            print("out of range")
        else:
            print("Temperatura = ", Temperature, "ºc")
#        print("medicoes = ", contador)

    with open(csvname, mode='a') as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([Pressure,Temperature])
        return(write_to_log)


while True: #Inicia Loop
    #getvalue()


def checkupdate():
    urllib.urlretrieve("https://github.com/kelvinhenriqu/PressurePackage/blob/main/Version.txt", filename="tempversion.txt")
    
    new_version = ''
    with open('tempversion.txt') as f:
        for line in f:
            line = line.strip()
            if '__VERSION__' in line:
                _, new_version = line.split('=', maxsplit=1)
                new_version = new_version.strip()
                break

    print('Version of the new script is:', new_version)
    print('Current version is:', __VERSION__)