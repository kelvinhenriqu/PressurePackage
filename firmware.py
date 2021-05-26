#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Sensor import Measurement
import time
import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)
Start = 0

Presao = Measurement.GetValue()

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

            elif Ddata == "0":
                print("dados = 0")        

            else:
                print("value not found")
        
            if Start == 1:
                Presao0 = Measurement.GetValue()
                print("Now Pressure and Start are: %s and %s" %(Presao0,Start))
                bluetoothdata = str(Presao0)#dado que sera enviado via bluetooth precisa ser uma string
                client_sock.send(bluetoothdata)
            else:
                print ("Start isn't 1 inside main")
    except KeyboardInterrupt:
        print ("\nprograma interrompido pelo usuario")

