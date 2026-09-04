import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
x = window.get_width() / 2
y = window.get_height() / 2


running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Ereignisbasierte Steuerung
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y -= 50
            if event.key == pygame.K_s:
                y += 50
            if event.key == pygame.K_a:
                x -= 50
            if event.key == pygame.K_d:
                x += 50
        """

    # Zustandsbasierte Steuerung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y -= 1
    if keys[pygame.K_s]:
        y += 1
    if keys[pygame.K_a]:
        x -= 1
    if keys[pygame.K_d]:
        x += 1

    # Update

    # Render
    window.fill("white")

    pygame.draw.circle(window, "blue", (x, y), 50)

    pygame.display.flip()

pygame.quit()


