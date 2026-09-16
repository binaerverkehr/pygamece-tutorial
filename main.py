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
radius = 50

player = Player(CENTER_X - 50, CENTER_Y - 50, radius)
obstacle = pygame.Rect((CENTER_X + 250, CENTER_Y - 100), (200, 200))

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    movement = dt * speed

    movement_x = 0
    movement_y = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        movement_y -= movement
    if keys[pygame.K_s]:
        movement_y += movement
    if keys[pygame.K_a]:
        movement_x -= movement
    if keys[pygame.K_d]:
        movement_x += movement

    player.x += movement_x
    player.y += movement_y

    if player.x - player.radius < 0:
        player.x = player.radius
    if player.x + player.radius > WINDOW_WIDTH:
        player.x = WINDOW_WIDTH - player.radius
    if player.y - player.radius < 0:
        player.y = player.radius
    if player.y + player.radius > WINDOW_HEIGHT:
        player.y = WINDOW_HEIGHT - player.radius

    nearest_x = player.x
    if player.x < obstacle.left:
        nearest_x = obstacle.left
    elif player.x > obstacle.right:
        nearest_x = obstacle.right

    nearest_y = player.y
    if player.y < obstacle.top:
        nearest_y = obstacle.top
    elif player.y > obstacle.bottom:
        nearest_y = obstacle.bottom

    window.fill("white")

    pygame.draw.rect(window, "grey", obstacle)
    pygame.draw.circle(window, "blue", (player.x, player.y), player.radius)
    pygame.draw.circle(window, "black", (nearest_x, nearest_y), 5)

    pygame.display.flip()

pygame.quit()
