import pygame
import socket
from threading import Thread

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

# Player and other player positions
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
other_player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3)

# Network setup for the listening peer
socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the port to be reused
socket_one.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 33123
server_address = '0.0.0.0'  # Listen on all network interfaces
socket_one.bind((server_address, port))
socket_one.listen(1)

conn, addr = socket_one.accept()

# Function to handle incoming data
def handle_server(sock):
    while True:
        try:
            received_data = sock.recv(4096).decode('utf-8')
            if received_data:
                x, y = map(int, received_data.split(':'))
                other_player_pos.update(x, y)
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to send player position
def send_position(sock, position):
    message = f"{int(position.x)}:{int(position.y)}"
    sock.send(message.encode('utf-8'))

# Start the thread for receiving data
t1 = Thread(target=handle_server, args=[conn])
t1.start()

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    moved = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 5
        moved = True
    if keys[pygame.K_RIGHT]:
        player_pos.x += 5
        moved = True
    if keys[pygame.K_UP]:
        player_pos.y -= 5
        moved = True
    if keys[pygame.K_DOWN]:
        player_pos.y += 5
        moved = True

    # Send position if moved
    if moved:
        send_position(conn, player_pos)

    # Drawing
    screen.fill("black")
    pygame.draw.circle(screen, "green", (int(player_pos.x), int(player_pos.y)), 40)
    pygame.draw.circle(screen, "red", (int(other_player_pos.x), int(other_player_pos.y)), 40)
    pygame.display.flip()

    clock.tick(60)

# Cleanup
pygame.quit()
conn.close()
socket_one.close()
