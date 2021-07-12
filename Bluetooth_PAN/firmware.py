import socket
from threading import Thread
import os

os.system('sudo bt-adapter --set Discoverable 1')
Welcome = "connect to raspberry\nyou can send START, STOP, RESTART, SHUTDOWN\n"

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port to listen
separator_token = "<SEP>"

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def listen_for_client(cs):

    while True:
        try:
            msg = cs.recv(1024).decode('utf-8')
            true = "OK\n"
            false = "NOK\n"

            print ("\nreceived %s" %msg)        

            if msg == "START\n":        #Start Measure
                print("Received START, doing something")
                cs.send(true.encode())

            elif msg == "STOP\n":       #Stop Measure
                print("Received STOP, doing something")
                cs.send(true.encode())

            elif msg == "RESTART\n":       #Restart board
                print("Received RESTART, rebooting board")
                cs.send(true.encode()) 

            elif msg == "SHUTDOWN\n":       #Shutdown board
                print("Received SHUTDOWN, shutdown board")
                cs.send(true.encode())          

            else:
                cs.send(false.encode())
                print ("value received do nothing")

        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)


while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_socket.send(Welcome.encode()) 
    client_sockets.add(client_socket) 

    t = Thread(target=listen_for_client, args=(client_socket,)) # make the thread daemon so it ends whenever the main thread ends    
    t.daemon = True
    t.start()


for cs in client_sockets:   #close client sockets
    cs.close()
s.close()   #close server socket