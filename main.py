import pygame
import time

pygame.init()

window = pygame.display.set_mode((800, 600))
x = window.get_width() / 2
y = window.get_height() / 2
clock = pygame.time.Clock()

start_time = time.perf_counter()
frames = 0

running = True
while running:
    clock.tick(60)
    frames += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y -= 1
    if keys[pygame.K_s]:
        y += 1
    if keys[pygame.K_a]:
        x -= 1
    if keys[pygame.K_d]:
        x += 1

    window.fill("white")

    pygame.draw.circle(window, "blue", (x, y), 50)

    pygame.display.flip()

end_time = time.perf_counter()
duration_in_seconds = end_time - start_time
fps = frames / duration_in_seconds
print(f"FPS: {fps:.2f}")

pygame.quit()
