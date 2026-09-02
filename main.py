import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
x = window.get_width() / 2
y = window.get_height() / 2
right = True

running = True
while running:
    # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spielzustand berechnen
    if right:
        x += 1
        if x + 50 == window.get_width():
            right = False
    else:
        x -= 1
        if x - 50 == 0:
            right = True

    # Render
    window.fill("white")

    pygame.draw.circle(window, "blue", (x, y), 50)

    pygame.display.flip()

pygame.quit()
