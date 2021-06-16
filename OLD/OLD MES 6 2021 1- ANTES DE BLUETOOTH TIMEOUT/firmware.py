#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 3.0

from Sensor import Measurement
import time
import bluetooth
from datetime import datetime

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)
Running = 0
Config = 0

print ("waiting for any bluetooth connection")
client_sock,address = server_sock.accept()
print ("Accepted connection from ",address)

def csvname():
    csvname = ""
    timestamp = datetime.now().strftime('%d%m%y%H%M%S')
    Serial = "21002" #Product Serial Number    
    csvname = Serial + timestamp #Create the filename, example: 21002020621134600 that is 21002.02/06/21.13:46:00
    #print(csvname)
    return csvname

if __name__ == "__main__":
    try:
        Debug = 0    
        while True: 
            name = csvname()                  
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

            elif Ddata == "p": #Request Pressure
                if Running == 1:
                    if Config == 1:
                        Config = 0
                        filename = int(name)
                        print("CSV File name setup is: ",filename)
                    P = Measurement.GetValue(1,filename,Running) #recebe pressão
                    print("Pressure is: %s"%P)
                    client_sock.send(str(P))
                else:
                    print("not running")
                    bluetoothdata = "F"
                    client_sock.send(bluetoothdata)

            elif Ddata == "t": #Request Temperature
                if Running == 1:
                    if Config == 1:
                        Config = 0
                        filename = int(name)
                        print("CSV File name setup is: ",filename)
                    T = Measurement.GetValue(2,filename,Running) #recebe temperatura
                    print("Temperature is: %s"%T)
                    client_sock.send(str(T))  
                else:
                    print("not running")
                    bluetoothdata = "F"
                    client_sock.send(bluetoothdata)             

            else:              #If Receive Unknow Data
                print("value not found")

    except KeyboardInterrupt:
        print ("\nprograma interrompido pelo usuario\n")
    except UnicodeDecodeError:
        print ("\nrecebido valor impossivel de ser reconhecido\n")
    except bluetooth.btcommon.BluetoothError:
        print ("\nconexão cancelada pelo usuario\n")

