import pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
x = window.get_width() / 2
y = window.get_height() / 2
clock = pygame.time.Clock()
speed = 300
radius = 50

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    movement = dt * speed

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y -= movement
    if keys[pygame.K_s]:
        y += movement
    if keys[pygame.K_a]:
        x -= movement
    if keys[pygame.K_d]:
        x += movement
    
    if x + radius > WINDOW_WIDTH:
        x = WINDOW_WIDTH - radius
    if x - radius < 0:
        x = radius
    if y - radius < 0:
        y = radius
    if y + radius > WINDOW_HEIGHT:
        y = WINDOW_HEIGHT - radius
    
    window.fill("white")

    pygame.draw.circle(window, "blue", (x, y), radius)

    pygame.display.flip()

pygame.quit()
