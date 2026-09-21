import pygame

from player import Player

pygame.init()

TILE_SIZE = 60
PLAYER_RADIUS = 20

level = [
    "################",
    "#P     #       #",
    "# #### # ##### #",
    "#    #   #     #",
    "#### ##### ### #",
    "#          #  G#",
    "################",
]

WINDOW_WIDTH = len(level[0]) * TILE_SIZE
WINDOW_HEIGHT = len(level) * TILE_SIZE

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
speed = 600

player = Player(0, 0, PLAYER_RADIUS)
walls = []

for row_index, row in enumerate(level):
    for col_index, char in enumerate(row):
        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE
        if char == "#":
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        elif char == "P":
            player.x = x + TILE_SIZE / 2
            player.y = y + TILE_SIZE / 2

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

        for wall in walls:
            if player.overlaps_rect(wall):
                player.x = previous_x

        previous_y = player.y
        player.y += step_y

        if player.y - player.radius < 0:
            player.y = player.radius
        if player.y + player.radius > WINDOW_HEIGHT:
            player.y = WINDOW_HEIGHT - player.radius

        for wall in walls:
            if player.overlaps_rect(wall):
                player.y = previous_y

    window.fill("white")

    for wall in walls:
        pygame.draw.rect(window, "grey", wall)

    pygame.draw.circle(window, "blue", (player.x, player.y), PLAYER_RADIUS)

    pygame.display.flip()

pygame.quit()
