#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 7.0

from Sensor import Measurement
import time
from datetime import datetime
import sys
import os
import socket


os.system('sudo bt-adapter --set Discoverable 1')
server_sock=socket.socket()
port = 5002
Addrs = "0.0.0.0"
server_sock.bind((Addrs,port))
server_sock.listen(1)
Running = 0
Config = 0
Timer = 0

print(f"[*] Listening as {Addrs}:{port}")

while True:
    try:
        server_sock.settimeout(0.01)
        client_sock,address = server_sock.accept()
        client_sock.settimeout(0.01) #maximum time to wait for bluetooth data
        print ("[+]Accepted connection from ",address)
        connected = True
        Timer = 0
        break
    except: 
        time.sleep(1) 
        if Timer == 300: #Auto shutdown after 5 minutes without bluetooth connection
            print ("shutting down because inactivity")
            os.system("sudo halt")
        else: 
            Timer += 1
            print ("waiting for any bluetooth connection(%i - 300)"%Timer)
            pass

def GenCSVName():
    csvname = ""
    timestamp = datetime.now().strftime('%d%m%y%H%M%S')
    Serial = "21002" #Product Serial Number    
    csvname = Serial + timestamp #Create the filename, example: 21002020621134600 that is 21002.02/06/21.13:46:00
    return csvname

if __name__ == "__main__":
    name = GenCSVName() 
    Debug = 0    
    
    while True:
        try:                              
            Bdata = client_sock.recv(1024).decode('utf-8') #Binary data converted to Decimal with maximum size of 1mb             

            if len(Bdata) != 0:
                print ("\nreceived %s" %Bdata)

                if Bdata == "start\n":   #Start Measure
                    Timer = 0
                    if Running != 1:
                        bluetoothdata = "   Starting measurement,    "
                        print (bluetoothdata)
                        client_sock.send(bluetoothdata.encode())
                        Running = 1
                        Config = 1

                elif Bdata == "stop\n": #Stop Measure
                    Timer = 0
                    if Running == 1:
                        bluetoothdata = "   Stopping measurement,    "
                        print (bluetoothdata)
                        client_sock.send(bluetoothdata.encode())
                        client_sock.send(name.encode())
                        Running = 0
                        Config = 0

                elif Bdata == "debug\n": #Debug On & Off
                    Timer = 0
                    if Debug == 1:
                        bluetoothdata = "   Debug Deactivated,    "
                        print (bluetoothdata)
                        client_sock.send(bluetoothdata.encode())
                        Measurement.Debug(0)
                        Debug = 0  
                    elif Debug == 0:
                        bluetoothdata = "   Debug activated,    "
                        print (bluetoothdata)
                        client_sock.send(bluetoothdata.encode())
                        Measurement.Debug(1)
                        Debug = 1 

                elif Bdata == "c\n": #Test CSV filename Generation 
                    Timer = 0
                    bluetoothdata = "    csvtest name is: " + name
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata.encode())

                elif Bdata == "exit\n": #Force Stop program
                    Timer = 0
                    bluetoothdata = "Force Stop"
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata.encode())
                    sys.exit()

                elif Bdata == "last\n": #Show last CSV file created
                    Timer = 0
                    bluetoothdata = "Last CSV Created is:  "
                    client_sock.send(bluetoothdata.encode())                
                    client_sock.send(name.encode())
                    print ("Last CSV Created is %s" %name)  

                elif Bdata == "shutdown\n": #shutdown rasp  
                    Timer = 0
                    bluetoothdata = "shutting down:  "
                    client_sock.send(bluetoothdata.encode())
                    print (bluetoothdata.encode()) 
                    os.system("sudo shutdown -h now")

                else:              #If Receive Unknow Data
                    Timer = 0
                    print("Value not found")

            else:
                try:
                    print( "connection lost... reconnecting" ) 
                    server_sock.settimeout(0.01)
                    client_sock,address = server_sock.accept()
                    client_sock.settimeout(0.01)
                    print( "re-connection successful" )
                    Timer = 0
                except: 
                    print("unsuccessful reconnection")                    
                    if Running == 1:
                        P = Measurement.GetValue(1,filename) #Ask Pressure
                        print("Pressure is: %s"%P)
                    else:
                        time.sleep(1)
                        Timer += 1
                        os.system("sudo halt") if Timer == 300 else print ("waiting for any bluetooth connection (%i - 300)"%Timer)
                    pass     
 

        except KeyboardInterrupt:
            print ("\nProgram interrupted by user\n")

        except socket.timeout: #if nothing received

            if Running == 1: #if any measure is running       
                
                if Config == 1: #if config process is necessary
                    Config = 0
                    filename = int(name)
                    print("CSV File name setup is: ",filename)

                P = Measurement.GetValue(1,filename) #Ask Pressure
                print("Pressure is: %s"%P)
                try:
                    client_sock.send(str(P).encode()) #try to send over bluetooth
                except:pass

            else:
                time.sleep(1)                

                if Timer == 60: #auto Bluetooth disconnect after 2 minutes 
                    print ("disconnecting bluetooth because nothing happened for a long time")
                    client_sock.close()
                    server_sock.close()
                    os.system("python3 firmware.py")
                    exit()
                else:
                    print ("nothing received (%i - 60)"%Timer)
                    Timer += 1
