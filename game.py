import pygame

TILE_SIZE = 60
PLAYER_RADIUS = 20
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

    def handle_events(self):
        # Fenster-Ereignisse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        # Tastatur-Ereignisse
        self.keys = pygame.key.get_pressed()

    def update(self, dt):
        pass

    def render(self):
        # Hintergrund zeichnen
        self.window.fill("white")

        # Display aktualisieren
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.update(self.dt)
            self.render()

        pygame.quit()


Game().run()
