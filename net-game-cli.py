import pygame
import socket
import logging
from threading import Thread

# Set up logging
logging.basicConfig(filename='net-game-cli.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
port = 33123
server_address = '0.0.0.0'  # Listen on all network interfaces
socket_one.bind((server_address, port))
socket_one.listen(1)
logging.info("Server listening on port {port}")
conn, addr = socket_one.accept()
logging.info(f"Connection established with {addr}")

# Function to handle incoming data
def handle_server(sock):
    while True:
        try:
            received_data = sock.recv(4096).decode('utf-8')
            if received_data:
                x, y = map(int, received_data.split(':'))
                other_player_pos.update(x, y)
                logging.info(f"Data received: {received_data} from {addr}")
        except Exception as e:
            logging.error(f"Error: {e}")
            break

# Function to send player position
def send_position(sock, position):
    message = f"{int(position.x)}:{int(position.y)}"
    sock.send(message.encode('utf-8'))
    logging.info(f"Sent data: {message}")

# Start the thread for receiving data
t1 = Thread(target=handle_server, args=[conn])
t1.start()

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            logging.info("Game is quitting")

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
socket_one.close()
logging.info("Server and game closed")
