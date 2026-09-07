import pygame
import time

"""
Delta Time = Zeitspanne für das Zeichnen eines Frames

Problem: Kopplung von Bewegung <--> Frames (Iteration/ Frames = Geschwindigkeit)

Lösung: Kopplung von Bewegung <--> Delta Time

60 FPS (f) --> 1/60 -> 0,0167s
30 FPS (f) --> 1/30 -> 0,0333s

### speed = 300px/s

60 FPS --> 0,0167s * 300 = 5,01px
30 FPS --> 0,0333s * 300 = 9,99px
"""

pygame.init()

window = pygame.display.set_mode((800, 600))
x = window.get_width() / 2
y = window.get_height() / 2
clock = pygame.time.Clock()

speed = 300
dt = 0

start_time = time.perf_counter()
frames = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    frames += 1


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

end_time = time.perf_counter()
duration_in_seconds = end_time - start_time
fps = frames / duration_in_seconds
print(f"FPS: {fps:.2f}")

pygame.quit()
