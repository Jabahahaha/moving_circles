import socket
from threading import Thread

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33124
server_address = '127.0.0.1'

def handle_server(connected_socket):
    while True:
        received_data = connected_socket.recv(4096)
        print(received_data.decode())

socket_one.connect((server_address, port))

# create thread to handle server
t1 = Thread(target=handle_server, args=[socket_one])
t1.start()

while True:
    message = input("Enter a message: ")
    socket_one.send(message.encode())

socket_one.close()