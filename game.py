import pygame

from constants import *
from level import TEST_LEVELS, Level
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        self.levels = TEST_LEVELS
        self.level_index = 0
        self.level: Level = self.levels[self.level_index]

        self.load_level(self.level_index)

        width = self.level.cols * TILE_SIZE
        height = self.level.rows * TILE_SIZE
        self.window = pygame.display.set_mode((width, height))

        player_x = self.level.player_start_x
        player_y = self.level.player_start_y
        self.player = Player(player_x, player_y, PLAYER_RADIUS, "blue")

        self.won = False
        self.font = pygame.font.Font(None, 72)
        self.win_text = self.font.render("Gewonnen!", True, "black")

    def move_player(self, dt):
        player = self.player
        distance = player.speed * dt

        dx = 0
        dy = 0

        if self.keys[pygame.K_w]:
            dy -= distance
        if self.keys[pygame.K_s]:
            dy += distance
        if self.keys[pygame.K_a]:
            dx -= distance
        if self.keys[pygame.K_d]:
            dx += distance

        steps = int(distance) + 1
        step_x = dx / steps
        step_y = dy / steps

        for _ in range(steps):
            previous_x = player.x
            player.x += step_x

            if player.x - player.radius < 0:
                player.x = player.radius
            if player.x + player.radius > WINDOW_WIDTH:
                player.x = WINDOW_WIDTH - player.radius

            for wall in self.level.walls:
                if player.overlaps_rect(wall):
                    player.x = previous_x
                    break

            for door in self.level.doors:
                if not player.inventory:
                    if player.overlaps_rect(door):
                        player.x = previous_x
                        break
                else:
                    if player.overlaps_rect(door):
                        self.level.doors.remove(door)
                        self.player.inventory.pop()

            previous_y = player.y
            player.y += step_y

            if player.y - player.radius < 0:
                player.y = player.radius
            if player.y + player.radius > WINDOW_HEIGHT:
                player.y = WINDOW_HEIGHT - player.radius

            for wall in self.level.walls:
                if player.overlaps_rect(wall):
                    player.y = previous_y
                    break

            for door in self.level.doors:
                if not player.inventory:
                    if player.overlaps_rect(door):
                        player.y = previous_y
                        break
                else:
                    if player.overlaps_rect(door):
                        self.level.doors.remove(door)
                        self.player.inventory.pop()

    def load_level(self, index):
        self.level = self.levels[index]
        # Fenstergröße an Levelgröße anpassen
        width = self.level.cols * TILE_SIZE
        height = self.level.rows * TILE_SIZE
        self.window = pygame.display.set_mode((width, height))

        # Entities
        self.player = Player(
            self.level.player_start_x,
            self.level.player_start_y,
            PLAYER_RADIUS,
            "blue",
        )

    def handle_events(self):
        # Fenster-Ereignisse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        # Tastatur-Ereignisse
        self.keys = pygame.key.get_pressed()
        """
        Spiel-Ereignisse
        """
        # Spieler erreicht Level-Ziel
        if not self.won and self.player.overlaps_rect(self.level.goal):
            # Wenn letztes Level erreicht, Sieg ansonsten nächstes Level
            if self.level_index + 1 >= len(self.levels):
                self.won = True
            else:
                self.level_index += 1
                self.load_level(self.level_index)

    def update(self, dt):
        self.move_player(dt)

        # Schlüssel und Türen
        for key in self.level.keys:
            if self.player.overlaps_rect(key):
                self.player.take(key)
                break
        for item in self.player.inventory:
            if item in self.level.keys:
                self.level.keys.remove(item)

    def render(self):
        # Hintergrund zeichnen
        self.window.fill("white")

        self.level.render(self.window)
        self.player.render(self.window)

        if self.won:
            text_rect = self.win_text.get_rect(center=self.window.get_rect().center)
            self.window.blit(self.win_text, text_rect)

        # Display aktualisieren
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.update(self.dt)
            self.render()

        pygame.quit()


if __name__ == "__main__":
    Game().run()
