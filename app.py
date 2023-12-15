import pygame
import socket
import json
import os
import logging
from threading import Thread

# Logging setup
logging.basicConfig(filename='app-client.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to save the player's position
def save_position(position):
    with open('player_position.json', 'w') as file:
        json.dump({'x': position.x, 'y': position.y}, file)
        logging.info("Player position saved")

# Function to load the player's position
def load_position():
    if os.path.exists('player_position.json'):
        with open('player_position.json', 'r') as file:
            position_data = json.load(file)
            logging.info("Player position loaded")
            return pygame.Vector2(position_data['x'], position_data['y'])
    return None

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

# Load position at start, or set default
loaded_position = load_position()
player_pos = loaded_position if loaded_position else pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
other_player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3)

# Network setup for the connecting peer
socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 33123
server_address = '127.0.0.1'  # Use the IP address of the machine running the listener script
try:
    socket_one.connect((server_address, port))
    logging.info(f"Connected to server at {server_address}:{port}")
except Exception as e:
    logging.error(f"Failed to connect to server: {e}")
    running = False  # Stop the game if connection fails

# Function to handle incoming data
def handle_server(sock):
    while True:
        try:
            received_data = sock.recv(4096).decode('utf-8')
            if received_data:
                x, y = map(int, received_data.split(':'))
                other_player_pos.update(x, y)
                logging.info(f"Data received: {received_data}")
        except Exception as e:
            logging.error(f"Error in receiving data: {e}")
            break

# Function to send player position
def send_position(sock, position):
    message = f"{int(position.x)}:{int(position.y)}"
    sock.send(message.encode('utf-8'))
    logging.info(f"Sent data: {message}")

# Start the thread for receiving data
t1 = Thread(target=handle_server, args=[socket_one])
t1.start()

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            logging.info("Client shutdown initiated")

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
        send_position(socket_one, player_pos)

    # Drawing
    screen.fill("black")
    pygame.draw.circle(screen, "green", (int(player_pos.x), int(player_pos.y)), 40)
    pygame.draw.circle(screen, "red", (int(other_player_pos.x), int(other_player_pos.y)), 40)
    pygame.display.flip()

    clock.tick(60)

# Cleanup
save_position(player_pos)  # Save position before quitting
pygame.quit()
socket_one.close()
logging.info("Client successfully closed")
