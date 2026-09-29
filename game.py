import pygame

from constants import HUD_HEIGHT, PLAYER_RADIUS, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
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
        self.playfield = pygame.Surface((width, height))
        self.window = pygame.display.set_mode((width, height + HUD_HEIGHT))

        player_x = self.level.player_start_x
        player_y = self.level.player_start_y
        self.player = Player(player_x, player_y, PLAYER_RADIUS, "blue")

        self.won = False
        font = pygame.font.Font(None, 72)
        self.win_text = font.render("Gewonnen!", True, "black")
        self.hud_font = pygame.font.Font(None, 32)

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
                if player.overlaps_rect(door):
                    if player.use_key():
                        self.level.doors.remove(door)
                        break
                    player.x = previous_x
                    break

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
                if player.overlaps_rect(door):
                    if player.use_key():
                        self.level.doors.remove(door)
                        break
                    player.y = previous_y
                    break

            for key in self.level.keys:
                if player.overlaps_rect(key):
                    self.level.keys.remove(key)
                    self.player.pickup_key()
                    break

    def load_level(self, index):
        self.level = self.levels[index]
        # Fenstergröße an Levelgröße anpassen
        width = self.level.cols * TILE_SIZE
        height = self.level.rows * TILE_SIZE
        self.playfield = pygame.Surface((width, height))
        self.window = pygame.display.set_mode((width, height + HUD_HEIGHT))

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

    def render_hud(self):
        text = f"Schlüssel: {self.player.keys} | Level {self.level_index + 1} von {len(self.levels)}"
        text_surface = self.hud_font.render(text, True, "white")
        self.window.blit(text_surface, (15, 15))

    def render(self):
        # Hintergrund zeichnen
        self.window.fill("black")
        self.playfield.fill("white")

        self.level.render(self.playfield)
        self.player.render(self.playfield)

        if self.won:
            text_rect = self.win_text.get_rect(center=self.playfield.get_rect().center)
            self.playfield.blit(self.win_text, text_rect)

        self.window.blit(self.playfield, (0, HUD_HEIGHT))
        self.render_hud()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.update(self.dt)
            self.render()

        pygame.quit()


Game().run()
