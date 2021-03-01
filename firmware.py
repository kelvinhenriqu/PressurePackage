#!/usr/bin/env python
# -*- coding: utf-8 -*-
__VERSION__ = 1.5

import time
import pigpio
import csv
import bluetooth
from datetime import datetime

Debug = 1
started = "0"
Serial="21001" #Numero Serial do produto
path = "/mnt/usb_share/logs/"

now = datetime.now()
date = now.strftime("%d%m%y%H%M%S")
csvname =path + date + "-" + Serial +".csv"

host = ""
port = 1        # Raspberry Pi uses port 1 for Bluetooth Communication
# Creaitng Socket Bluetooth RFCOMM communication
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Bluetooth Socket Created')
try:
        server.bind((host, port))
        print("Bluetooth Binding Completed")
except:
        print("Bluetooth Binding Failed")
server.listen(1) # One connection at a time
# Server accepts the clients request and assigns a mac address.
client, address = server.accept()
print("Connected To", address)
print("Client:", client)

def main():
    try:
        while True:
            # Receivng the data.
            data = client.recv(1024) # 1024 is the buffer size.
            print(data)

            if data == "1":
                    print('recebido 1, iniciando medicao')
                    started = "1"
                    send_data = "iniciando medicao"
            elif data == "0":
                    print('recebido 0, parando medicao')
                    started = "0"
                    send_data = "parando medicao"
            else:# data != "0" and data != "1":
                    send_data = "envie 1 ou 0 "
            # Sending the data.
            client.send(send_data)

            if started == "1":

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
                        print("Temperatura = ", Temperature, "C")
                        #print("medicoes = ", contador)

                with open(csvname, mode='a') as sensor_readings:
                    sensor_write = csv.writer(sensor_readings, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    write_to_log = sensor_write.writerow([Pressure,Temperature])
                    return(write_to_log)

                send_data = Pressure
                client.send(send_data)
            #else:
               # print("started é diferente de 0, entao nada e feito")

    except:
        # Closing the client and server connection
        client.close()
        server.close()

if __name__ == "__main__":
    main()