import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
x = window.get_width() / 2
y = window.get_height() / 2
clock = pygame.time.Clock()
speed = 300

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

    window.fill("white")

    pygame.draw.circle(window, "blue", (x, y), 50)

    pygame.display.flip()

pygame.quit()
