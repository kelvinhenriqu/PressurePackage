#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 5.0

import time
import pigpio
import csv

Debug = 0

def SaveSD(P,T,Filename):
    global Debug
    path = "/home/pi/measurements/" # path to save the file
    Directory = str(path) + str(Filename) + ".csv"

    with open(Directory, mode='a') as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([P,T]) #write P & T in sdcard
        return(write_to_log)

    if Debug == 1: print("measure saved in CSV file")

class Measurement :
    def Debug(self):
        global Debug
        Debug = self

    def GetValue(measure,filename):

        global Debug
        try:        
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
            bpress = p1+p2+p3            #concatenate values in bytes
            dpress = int(bpress, 2)      #convert to Decimal
            Pressure = (((((dpress/12305550)*100)*6)/100)-2.2)*1.042 #calibration factor is 1.042
            btemp = t1+t2                #concatenate values in bytes
            dtemp = int(btemp, 2)        #convert to Decimal
            Temperature = (((dtemp/65536)*190)-40)*0.954 #calibration factor is 0.954
            Save = SaveSD(Pressure,Temperature,filename)
            
        except pigpio.error:
            print ("\ni2c error, is sensor connected ?\n")
#             except:
#                 print ("unknown error occoured")
        except KeyboardInterrupt:
            print ("\ncancelled by user\n")
        finally:
            if Debug == 1:
                if Pressure < -1 or Pressure > 5:
                    print ("\nout of range\n")
                else:
                    print ("\nPressure: %s bar\n"%(Pressure))

                if  Temperature <0 or Temperature >100:
                    print ("\nout of range\n")
                else:
                    print ("\nTemperature: %s ºC\n"%(Temperature))

        if measure == 1: return Pressure        #firmware request Pressure
        if measure == 2: return Temperature     #firmware request Temperature
    

if __name__ == "__main__":

#    while True:
        filename = "9999" #test filename
        P = Measurement.GetValue(1,filename) #ask for temperature
        T = Measurement.GetValue(2,filename) #ask for pressure
        print("\npressure: %s \ntemperature: %s\n"%(P,T))


