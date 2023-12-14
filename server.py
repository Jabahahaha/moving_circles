import socket
from threading import Thread

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33124

socket_one.bind(("0.0.0.0", port))
socket_one.listen(1)

def handle_client(connected_socket):
    while True:
        received_data = connected_socket.recv(4096)
        print(received_data.decode())


connected_socket, addr = socket_one.accept()
print("Connection from: " + str(addr))

# create thread to handle client
# t1 = Thread(target=handle_client, args=[connected_socket])
# t1.start()

while True:
    message = input("Enter a message: ")
    connected_socket.send(message.encode())

#    connected_socket.close()

    # if "stop" in received_data.decode():
    #     break

socket_one.close()