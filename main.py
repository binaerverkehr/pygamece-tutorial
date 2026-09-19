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
obstacles = [
    pygame.Rect((CENTER_X + 250, CENTER_Y - 100), (200, 200)),
    pygame.Rect((CENTER_X + 250, CENTER_Y - 400), (200, 200)),
    pygame.Rect((CENTER_X + 250, CENTER_Y + 200), (200, 200)),
]

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

    steps = int(movement) + 1
    step_x = movement_x / steps
    step_y = movement_y / steps

    for step in range(steps):
        previous_x = player.x
        player.x += step_x

        if player.x - player.radius < 0:
            player.x = player.radius
        if player.x + player.radius > WINDOW_WIDTH:
            player.x = WINDOW_WIDTH - player.radius

        for obstacle in obstacles:
            if player.overlaps_rect(obstacle):
                player.x = previous_x

        previous_y = player.y
        player.y += step_y

        if player.y - player.radius < 0:
            player.y = player.radius
        if player.y + player.radius > WINDOW_HEIGHT:
            player.y = WINDOW_HEIGHT - player.radius

        for obstacle in obstacles:
            if player.overlaps_rect(obstacle):
                player.y = previous_y

    window.fill("white")

    for obstacle in obstacles:
        pygame.draw.rect(window, "grey", obstacle)

    pygame.draw.circle(window, "blue", (player.x, player.y), player.radius)

    pygame.display.flip()

pygame.quit()
