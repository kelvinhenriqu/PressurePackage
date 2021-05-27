#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 2.2

from Sensor import Measurement
import time
import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)
Start = 0

print ("waiting for any bluetooth connection")
client_sock,address = server_sock.accept()
print ("Accepted connection from ",address)

if __name__ == "__main__":
    try:
        while True:
        
            #print("Initial Pressure and Temperature is: %s and %s" %(globals.Pressure,globals.Temperature))
            Bdata = client_sock.recv(1024) #dados em binario
            Ddata = Bdata.decode('utf-8')
            print ("received %s that means %s" %(Bdata,Ddata))   

            if Ddata == "1":
                if Start != 1:
                    bluetoothdata = "Received 1, Starting measurement"
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Start = 1

            elif Ddata == "2":
                if Start == 1:
                    bluetoothdata = "Received 2, Stopping measurement"
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Start = 0

            elif Ddata == "3":
                print("Received 3, Debug activated")
                Measurement.Debug(1)

            elif Ddata == "4":
                print("Received 4, Debug deactivated")  
                Measurement.Debug(0)      

            else:
                print("value not found")
        
            if Start == 1:
                P = Measurement.GetValue(1)
                T = Measurement.GetValue(2)
                print("Now Pressure, Temperature and Start are: %s, %s and %s" %(P,T,Start))
                bluetoothdata = str(P,T)#dado que sera enviado via bluetooth precisa ser uma string
                client_sock.send(bluetoothdata)
            else:
                print ("Start isn't 1 inside main")
    except KeyboardInterrupt:
        print ("\nprograma interrompido pelo usuario")
    except UnicodeDecodeError:
        print ("\nrecebido valor impossivel de ser reconhecido")

