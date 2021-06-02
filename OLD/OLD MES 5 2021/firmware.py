#!/usr/bin/env python
# -*- coding: utf-8 -*-
__VERSION__ = 1.8

import time
import pigpio
import csv
import bluetooth
from datetime import datetime
from multiprocessing import Process, Pipe

Debug = 1
started = 0
Serial="21001" #Product Serial Number
path = "/mnt/usb_share/logs/"

now = datetime.now()
date = now.strftime("%d%m%y%H%M%S")
csvname =path + date + "-" + Serial +".csv"

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

print "waiting for any bluetooth connection"
client_sock,address = server_sock.accept()
print "Accepted connection from ",address


def main(conn): 
    #try:
        while True:
            global started
            global Debug        
            data = client_sock.recv(1024)
            print "received [%s]" % data

            if data == "1":#start
                bluetoothdata = "Received start, Starting measurement"
                print bluetoothdata
                client_sock.send(bluetoothdata)
                started = 1
                print "started now is", started
                conn.send(1)
                conn.close()

                #PressureValue()
            elif data == "2":#stop
                bluetoothdata = "Received stop, Stoping measurement"
                print bluetoothdata
                client_sock.send(bluetoothdata)
                started = 0
                print "started now is", started
                #PressureValue()
            elif data == "3":#TDebug
                bluetoothdata = "Received TDebug, Allowing debug"
                print bluetoothdata
                client_sock.send(bluetoothdata)
                Debug = 1
                #PressureValue()
            elif data == "4":#FDebug
                bluetoothdata = "Received FDebug, Not Allowing debug"
                print bluetoothdata
                client_sock.send(bluetoothdata)
                Debug = 1
                #PressureValue()
            else:
                bluetoothdata = "received value isn't recognized"
                print bluetoothdata
                client_sock.send(bluetoothdata) 
#    except:
#        # Closing the client and server connection
#        client_sock.close()
#        server_sock.close()

def PressureValue():    
    while True:
        parent_conn, child_conn = Pipe()
        p = Process(target=main, args=(child_conn,))
        p.start()
        #p.join()
        print "Inside Pressure Def started =", started
        startmeasure = parent_conn.recv()


        if  startmeasure == 1:
            print "doing Measurement"
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

            if Debug == 1:
                print()
                if Pressure < -1 or Pressure > 5:
                    print "out of range"
                else:
                    print "Pressao = ", Pressure, "bar"

                if  Temperature <0 or Temperature >100:
                    print "out of range"
                else:
                    print "Temperatura = ", Temperature, "C"
                    #print("medicoes = ", contador)

    #        with open(csvname, mode='a') as sensor_readings:
    #            sensor_write = csv.writer(sensor_readings, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #            write_to_log = sensor_write.writerow([Pressure,Temperature])
    #            return(write_to_log)

            client_sock.send(str('  pressure='))
            client_sock.send(str(Pressure))
            print "started is 1 in def PressureValue"
            #main()
        else:
            time.sleep(2)
            #main()

if __name__ == "__main__":
    #main()
    #Process(target=main).start() 
    Process(target=PressureValue).start() 