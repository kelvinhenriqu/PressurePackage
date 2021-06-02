#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 2.0

import time
import pigpio
import csv
from datetime import datetime

Debug = 0

Serial="21001" #Product Serial Number
path = "/mnt/usb_share/logs/"

now = datetime.now()
date = now.strftime("%d%m%y%H%M%S")
csvname =path + date + "-" + Serial +".csv"

class Measurement :
    def GetValue():
        try:
            print ("doing Measurement\n")
        
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
            press = p1+p2+p3            #concatenate values in bytes
            dpress = int(press, 2)      #convert to Decimal
            Pressure = (((((dpress/12305550)*100)*6)/100)-2.2)*1.042
            temp = t1+t2                #concatenate values in bytes
            dtemp = int(temp, 2)        #convert to Decimal
            Temperature = (((dtemp/65536)*190)-40)*0.954
            
            if Debug > 0:
                print()
                if Pressure < -1 or Pressure > 5:
                    print ("out of range\n")
                else:
                    print ("Pressure: %s bar\n"%(Pressure))

                if  Temperature <0 or Temperature >100:
                    print ("out of range\n")
                else:
                    print ("Temperature: %s ºC\n"%(Temperature))
                    #print("medicoes = ", contador)

        except pigpio.error:
            print ("i2c error, is sensor connected ?\n")
#       except:
#           print ("unknown error occoured")
        finally:
            print ("Currently Pressure is %s\n"%Pressure)

        return Pressure
    

if __name__ == "__main__":
    Measurement.GetValue()



