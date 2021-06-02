import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
client_sock,address = server_sock.accept()

client_sock.close()
server_sock.close()
