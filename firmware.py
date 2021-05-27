#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__VERSION__ = 2.6

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
            Bdata = client_sock.recv(1024) #dados em binario
            Ddata = Bdata.decode('utf-8') #conversão de dados para decimal
            print ("\nreceived %s that means %s" %(Bdata,Ddata))   

            if Ddata == "1":
                if Start != 1:
                    bluetoothdata = "   Starting measurement,    "
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Start = 1

            elif Ddata == "2":
                if Start == 1:
                    bluetoothdata = "   Stopping measurement,    "
                    print (bluetoothdata)
                    client_sock.send(bluetoothdata)
                    Start = 0

            elif Ddata == "3":
                bluetoothdata = "   Debug activated,    "
                print (bluetoothdata)
                client_sock.send(bluetoothdata)
                Measurement.Debug(1)

            elif Ddata == "4":
                bluetoothdata = "   Debug deactivated,    "
                print (bluetoothdata)
                client_sock.send(bluetoothdata)
                Measurement.Debug(0)      

            else:
                print("value not found")
        
            if Start == 1:
                P = Measurement.GetValue(1) #recebe pressão
                T = Measurement.GetValue(2) #recebe temperatura
                print("Now Pressure, Temperature and Start are: %s, %s and %s" %(P,T,Start))
                bluetoothdata = 'P ' + str(P) + ',' + 'T ' + str(T) #dado que sera enviado via bluetooth precisa ser uma string
                client_sock.send(bluetoothdata)


    except KeyboardInterrupt:
        print ("\nprograma interrompido pelo usuario")
    except UnicodeDecodeError:
        print ("\nrecebido valor impossivel de ser reconhecido")
    except bluetooth.btcommon.BluetoothError:
        print ("\nconexão cancelada pelo usuario")

