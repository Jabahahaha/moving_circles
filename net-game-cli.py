import pygame
import socket
from threading import Thread

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

circle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
other_player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3)

def handle_server(connected_socket):
    while True:
        try:
            received_data = connected_socket.recv(4096).decode('utf-8')
            if received_data:
                x, y = map(int, received_data.split(':'))
                other_player_pos.update(x, y)
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def send_position(socket, position):
    message = f"{int(position.x)}:{int(position.y)}#"
    socket.send(message.encode('utf-8'))

socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 33124
server_address = '127.0.0.1'

socket_one.connect((server_address, port))

t1 = Thread(target=handle_server, args=[socket_one])
t1.start()

while running:
    old_pos = circle_pos.xy

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    moved = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle_pos.x -= 5
        moved = True
    if keys[pygame.K_RIGHT]:
        circle_pos.x += 5
        moved = True
    if keys[pygame.K_UP]:
        circle_pos.y -= 5
        moved = True
    if keys[pygame.K_DOWN]:
        circle_pos.y += 5
        moved = True

    if moved:
        send_position(socket_one, circle_pos)

    screen.fill("black")
    pygame.draw.circle(screen, "green", (int(circle_pos.x), int(circle_pos.y)), 40)
    pygame.draw.circle(screen, "red", (int(other_player_pos.x), int(other_player_pos.y)), 40)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
