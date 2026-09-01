import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
x = 0
y = 0

running = True
while running:
    # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spielzustand berechnen
    x += 1

    # Render
    window.fill("white")
    rect = pygame.Rect((x, y), (100, 100))
    pygame.draw.rect(window, "#8c2020", rect)
    pygame.draw.circle(window, "blue", (100, 100), 100)

    pygame.display.flip()

pygame.quit()
