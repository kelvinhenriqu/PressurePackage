#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 5.0

from Sensor import Measurement
import time
import bluetooth
from datetime import datetime
import sys
import os

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)
Running = 0
Config = 0
Timer = 0

print ("waiting for any bluetooth connection")
client_sock,address = server_sock.accept()
client_sock.settimeout(0.01) #maximum time to wait for bluetooth data
print ("Accepted connection from ",address)

def GenCSVName():
    csvname = ""
    timestamp = datetime.now().strftime('%d%m%y%H%M%S')
    Serial = "21002" #Product Serial Number    
    csvname = Serial + timestamp #Create the filename, example: 21002020621134600 that is 21002.02/06/21.13:46:00
    #print(csvname)
    return csvname

if __name__ == "__main__":
    name = GenCSVName() 
    Debug = 0    
    
    while True:
        try:                              
            Bdata = client_sock.recv(1024) #binary data with maximum size of 1mb 
            Ddata = Bdata.decode('utf-8') #binary to decimal conversion
            print ("\nreceived %s that means %s" %(Bdata,Ddata))             

            if Ddata == "1":   #Start Measure
                if Running != 1:
                    bluetoothdata = "   Starting measurement,    "
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Running = 1
                    Config = 1

            elif Ddata == "2": #Stop Measure
                if Running == 1:
                    bluetoothdata = "   Stopping measurement,    "
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Running = 0
                    Config = 0

            elif Ddata == "d": #Debug On & Off
                if Debug == 1:
                    bluetoothdata = "   Debug Deactivated,    "
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Measurement.Debug(0)
                    Debug = 0  
                elif Debug == 0:
                    bluetoothdata = "   Debug activated,    "
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Measurement.Debug(1)
                    Debug = 1 

            elif Ddata == "c": #Test CSV filename Generation 
                bluetoothdata = "    csvtest name is: " + name
                print (bluetoothdata)
                client_sock.send(bluetoothdata)

            elif Ddata == "s": #Force Stop program
                bluetoothdata = "Force Stop"
                print (bluetoothdata)
                client_sock.send(bluetoothdata)
                sys.exit()

            elif Ddata == "l": #Show last CSV file created
                bluetoothdata = "Last CSV Created is:  "
                client_sock.send(bluetoothdata)                
                client_sock.send(name)
                print ("Last CSV Created is %s" %name)  

            elif Ddata == "x": #shutdown rasp  
                bluetoothdata = "shutting down:  "
                client_sock.send(bluetoothdata)
                print (bluetoothdata) 
                os.system("sudo shutdown -h now")

            else:              #If Receive Unknow Data
                print("Value not found")

        except KeyboardInterrupt:
            print ("\nProgram interrupted by user\n")
        except UnicodeDecodeError:
            print ("\nReceived unrecognizable value\n")
        except bluetooth.btcommon.BluetoothError: #if nothing received

            if Running == 1: #if any measure is running                
                if Config == 1: #if config process is necessary
                    Config = 0
                    filename = int(name)
                    print("CSV File name setup is: ",filename)
                P = Measurement.GetValue(1,filename) #Ask Pressure
                print("Pressure is: %s"%P)
                client_sock.send(str(P))
            else:
#                print("waiting for any command") #don't use it in autostart routine, may use a lot of pi's power
                time.sleep(1)                

                if Timer == 120: #auto shutdown after 2 minutes 
                    os.system("sudo shutdown -h now")
                else:
                    Timer += 1

                
