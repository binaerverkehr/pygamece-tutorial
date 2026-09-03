import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
x = window.get_width() / 2
y = window.get_height() / 2

running = True
while running:
    # Ereignisse prüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y -= 10
            elif event.key == pygame.K_s:
                y += 10
            elif event.key == pygame.K_a:
                x -= 10
            elif event.key == pygame.K_d:
                x += 10

    # Spielzustand berechnen
    
    # Render
    window.fill("white")

    pygame.draw.circle(window, "blue", (x, y), 50)

    pygame.display.flip()

pygame.quit()
