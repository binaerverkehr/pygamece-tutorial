import pygame

from constants import HUD_HEIGHT, PLAYER_RADIUS, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from level import LAYOUTS, Level
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        self.layouts = LAYOUTS
        self.level_index = 0
        self.player = Player(PLAYER_RADIUS, "blue")
        self.load_level(self.level_index)

        self.state = "playing"
        self.overlay_font = pygame.font.Font(None, 72)
        self.hud_font = pygame.font.Font(None, 32)
        self.heart_font = pygame.font.SysFont("arial,dejavusans", 32)

    def move_player(self, dt):
        player = self.player
        direction = pygame.Vector2(
            self.keys[pygame.K_d] - self.keys[pygame.K_a],  # x-Bewegung
            self.keys[pygame.K_s] - self.keys[pygame.K_w],  # y-Bewegung
        )

        if direction.length_squared() > 0:
            direction = direction.normalize()

        distance = direction * player.speed * dt

        steps = int(distance.length()) + 1
        step = distance / steps

        for _ in range(steps):
            previous_x = player.pos.x
            player.pos.x += step.x

            if player.pos.x - player.radius < 0:
                player.pos.x = player.radius
            if player.pos.x + player.radius > WINDOW_WIDTH:
                player.pos.x = WINDOW_WIDTH - player.radius

            for wall in self.level.walls:
                if player.overlaps_rect(wall):
                    player.pos.x = previous_x
                    break

            for door in self.level.doors:
                if player.overlaps_rect(door):
                    if player.use_key():
                        self.level.doors.remove(door)
                        break
                    player.pos.x = previous_x
                    break

            previous_y = player.pos.y
            player.pos.y += step.y

            if player.pos.y - player.radius < 0:
                player.pos.y = player.radius
            if player.pos.y + player.radius > WINDOW_HEIGHT:
                player.pos.y = WINDOW_HEIGHT - player.radius

            for wall in self.level.walls:
                if player.overlaps_rect(wall):
                    player.pos.y = previous_y
                    break

            for door in self.level.doors:
                if player.overlaps_rect(door):
                    if player.use_key():
                        self.level.doors.remove(door)
                        break
                    player.pos.y = previous_y
                    break

            for key in self.level.keys:
                if player.overlaps_rect(key):
                    self.level.keys.remove(key)
                    self.player.pickup_key()
                    break

    def load_level(self, index):
        self.level = Level(self.layouts[index])
        # Fenstergröße an Levelgröße anpassen
        width = self.level.cols * TILE_SIZE
        height = self.level.rows * TILE_SIZE
        self.playfield = pygame.Surface((width, height))
        self.window = pygame.display.set_mode((width, height + HUD_HEIGHT))

        self.player.respawn(self.level.player_start_x, self.level.player_start_y)

    def handle_events(self):
        # Fenster-Ereignisse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.state == "playing":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "playing"
            if event.type == pygame.WINDOWFOCUSLOST and self.state == "playing":
                self.state = "focus_paused"
            if event.type == pygame.WINDOWFOCUSGAINED and self.state == "focus_paused":
                self.state = "playing"
        # Tastatur-Ereignisse
        self.keys = pygame.key.get_pressed()
        """
        Spiel-Ereignisse
        """
        # Spieler erreicht Level-Ziel
        if self.state == "playing" and self.player.overlaps_rect(self.level.goal):
            # Wenn letztes Level erreicht, Sieg ansonsten nächstes Level
            if self.level_index + 1 >= len(self.layouts):
                self.state = "won"
            else:
                self.level_index += 1
                self.load_level(self.level_index)
        # Spieler berührt Gegner
        if self.state == "playing":
            for enemy in self.level.enemies:
                distance = self.player.pos.distance_to(enemy.pos)
                if distance < self.player.radius + enemy.radius:
                    self.player.lives -= 1
                    self.load_level(self.level_index)
                    break

    def update(self, dt):
        self.move_player(dt)

        obstacles = self.level.walls + self.level.doors
        for enemy in self.level.enemies:
            enemy.update(dt, obstacles)

    def render_overlay(self, text):
        text_surface = self.overlay_font.render(text, True, "black")
        text_rect = text_surface.get_rect(center=self.playfield.get_rect().center)
        self.playfield.blit(text_surface, text_rect)

    def render_hud(self):
        hearts = self.heart_font.render("♥" * self.player.lives, True, "red")
        self.window.blit(hearts, (15, 8))

        text = f"Schlüssel: {self.player.keys} | Level {self.level_index + 1} von {len(self.layouts)}"
        text_surface = self.hud_font.render(text, True, "white")
        self.window.blit(text_surface, (125, 15))

    def render(self):
        # Hintergrund zeichnen
        self.window.fill("black")
        self.playfield.fill("white")

        self.level.render(self.playfield)
        self.player.render(self.playfield)

        if self.state in ("paused", "focus_paused"):
            self.render_overlay("Pause")
        elif self.state == "won":
            self.render_overlay("Gewonnen!")

        self.window.blit(self.playfield, (0, HUD_HEIGHT))
        self.render_hud()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            if self.state == "playing":
                self.update(self.dt)
            self.render()

        pygame.quit()


Game().run()
