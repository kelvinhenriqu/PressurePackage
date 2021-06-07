#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 5.0

from Sensor import Measurement
import time
import bluetooth
from datetime import datetime
import sys

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)
Running = 0
Config = 0

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
            Bdata = client_sock.recv(1024) #dados em binario
            Ddata = Bdata.decode('utf-8') #conversão de dados para decimal
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

            elif Ddata == "s":
                bluetoothdata = "Force Stop"
                print (bluetoothdata)
                client_sock.send(bluetoothdata)
                sys.exit()

            elif Ddata == "l":
                bluetoothdata = "Last CSV Created is:  "
                client_sock.send(bluetoothdata)                
                client_sock.send(name)
                print ("Last CSV Created is %s" %name)
                             

            else:              #If Receive Unknow Data
                print("value not found")

        except KeyboardInterrupt:
            print ("\nprograma interrompido pelo usuario\n")
        except UnicodeDecodeError:
            print ("\nrecebido valor impossivel de ser reconhecido\n")
        except bluetooth.btcommon.BluetoothError: #if nothing received

            if Running == 1: #if any measuare is running                
                if Config == 1: #if config process is necessary
                    Config = 0
                    filename = int(name)
                    print("CSV File name setup is: ",filename)
                P = Measurement.GetValue(1,filename) #Ask Pressure
                print("Pressure is: %s"%P)
                client_sock.send(str(P))
            else:
                print("waiting for any command")
