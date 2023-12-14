import socket
from threading import Thread

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33124

socket_one.bind(("0.0.0.0", port))
socket_one.listen(1)

def handle_client(connected_socket):
    buffer = ""
    while True:
        try:
            received_data = connected_socket.recv(4096).decode()
            if received_data:
                buffer += received_data
                while '#' in buffer:
                    message, buffer = buffer.split('#', 1)
                    x, y = map(int, message.split(':'))
                    print(f"Received coordinates: X={x}, Y={y}")
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

connected_socket, addr = socket_one.accept()
print("Connection from: " + str(addr))

t1 = Thread(target=handle_client, args=[connected_socket])
t1.start()

while True:
    message = input("Enter a message: ")
    connected_socket.send(message.encode())

socket_one.close()
