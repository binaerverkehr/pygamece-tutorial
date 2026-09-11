import pygame
from player import Player

pygame.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
CENTER_X = WINDOW_WIDTH / 2
CENTER_Y = WINDOW_HEIGHT / 2

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
speed = 600

player = Player(CENTER_X-50, CENTER_Y-50, 100, 100)
obstacle = pygame.Rect((player.x + 300, player.y - player.height/2), (200, 200))

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    previous_x = player.x
    previous_y = player.y

    movement = dt * speed

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= movement
    if keys[pygame.K_s]:
        player.y += movement
    if keys[pygame.K_a]:
        player.x -= movement
    if keys[pygame.K_d]:
        player.x += movement
    
    if player.x + player.width > WINDOW_WIDTH:
        player.x = WINDOW_WIDTH - player.width
    if player.x < 0:
        player.x = 0
    if player.y < 0:
        player.y = 0
    if player.y + player.width > WINDOW_HEIGHT:
        player.y = WINDOW_HEIGHT - player.width

    collision = player.rect.colliderect(obstacle)
    if collision:
        player.x = previous_x
        player.y = previous_y
    
    window.fill("white")

    pygame.draw.rect(window, "grey", obstacle)

    pygame.draw.rect(window, "blue", player.rect)

    pygame.display.flip()

pygame.quit()
