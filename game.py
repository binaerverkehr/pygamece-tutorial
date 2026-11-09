import asyncio

import pygame

from constants import ASSETS_DIR, HUD_HEIGHT, PLAYER_RADIUS, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from level import LAYOUTS, Level
from player import Player


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        self.images = {}
        for name in ("player", "enemy", "key", "floor", "wall", "door", "goal", "heart"):
            self.images[name] = pygame.image.load(ASSETS_DIR / f"{name}.png").convert_alpha()

        self.sounds = {}
        for name in ("key", "door", "hit", "goal", "win", "game_over"):
            self.sounds[name] = pygame.mixer.Sound(ASSETS_DIR / f"{name}.ogg")

        pygame.mixer.music.load(ASSETS_DIR / "music.ogg")
        pygame.mixer.music.set_volume(0.4)

        self.layouts = LAYOUTS
        self.start_game()
        self.state = "menu"

        self.overlay_font = pygame.font.Font(None, 72)
        self.hud_font = pygame.font.Font(None, 32)

    def start_game(self):
        self.level_index = 0
        self.player = Player(PLAYER_RADIUS, self.images["player"])
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.load_level(self.level_index)
        self.state = "playing"
        pygame.mixer.music.play(-1)

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
                if player.overlaps_rect(wall.rect):
                    player.pos.x = previous_x
                    break

            for door in self.level.doors:
                if player.overlaps_rect(door.rect):
                    if player.use_key():
                        self.level.doors.remove(door)
                        self.sounds["door"].play()
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
                if player.overlaps_rect(wall.rect):
                    player.pos.y = previous_y
                    break

            for door in self.level.doors:
                if player.overlaps_rect(door.rect):
                    if player.use_key():
                        self.level.doors.remove(door)
                        self.sounds["door"].play()
                        break
                    player.pos.y = previous_y
                    break

            for key in self.level.keys:
                if player.overlaps_rect(key.rect):
                    self.level.keys.remove(key)
                    self.player.pickup_key()
                    self.sounds["key"].play()
                    break

    def load_level(self, index):
        self.level = Level(self.layouts[index], self.images)
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
                        pygame.mixer.music.pause()
                    elif self.state == "paused":
                        self.state = "playing"
                        pygame.mixer.music.unpause()
                if event.key == pygame.K_r and self.state in ("game_over", "won"):
                    self.start_game()
                if event.key == pygame.K_RETURN and self.state == "menu":
                    self.state = "playing"
            if event.type == pygame.WINDOWFOCUSLOST and self.state == "playing":
                self.state = "focus_paused"
                pygame.mixer.music.pause()
            if event.type == pygame.WINDOWFOCUSGAINED and self.state == "focus_paused":
                self.state = "playing"
                pygame.mixer.music.unpause()
        # Tastatur-Ereignisse
        self.keys = pygame.key.get_pressed()
        """
        Spiel-Ereignisse
        """
        # Spieler erreicht Level-Ziel
        if self.state == "playing" and self.player.overlaps_rect(self.level.goal.sprite.rect):
            # Wenn letztes Level erreicht, Sieg ansonsten nächstes Level
            if self.level_index + 1 >= len(self.layouts):
                self.state = "won"
                pygame.mixer.music.stop()
                self.sounds["win"].play()
            else:
                self.sounds["goal"].play()
                self.level_index += 1
                self.load_level(self.level_index)
        # Spieler berührt Gegner
        if self.state == "playing":
            if pygame.sprite.spritecollideany(self.player, self.level.enemies, pygame.sprite.collide_circle):
                self.player.lives -= 1
                self.sounds["hit"].play()
                if self.player.lives == 0:
                    self.state = "game_over"
                    pygame.mixer.music.stop()
                    self.sounds["game_over"].play()
                else:
                    self.load_level(self.level_index)

    def update(self, dt):
        self.move_player(dt)

        obstacles = self.level.walls.sprites() + self.level.doors.sprites()
        self.level.enemies.update(dt, obstacles)

    def render_overlay(self, text):
        text_surface = self.overlay_font.render(text, True, "black")
        text_rect = text_surface.get_rect(center=self.playfield.get_rect().center)
        self.playfield.blit(text_surface, text_rect)

    def render_hud(self):
        for i in range(self.player.lives):
            self.window.blit(self.images["heart"], (15 + i * 30, 18))

        text = f"Schlüssel: {self.player.keys} | Level {self.level_index + 1} von {len(self.layouts)}"
        text_surface = self.hud_font.render(text, True, "white")
        self.window.blit(text_surface, (125, 15))

    def render(self):
        # Hintergrund zeichnen
        self.window.fill("black")

        if self.state == "menu":
            self.render_menu()
        else:
            self.render_game()

        pygame.display.flip()

    def render_menu(self):
        center_x, center_y = self.window.get_rect().center

        title = self.overlay_font.render("Labyrinth", True, "white")
        self.window.blit(title, title.get_rect(center=(center_x, center_y - 40)))

        hint = self.hud_font.render("Bewegen mit WASD, Pause mit P, Start mit Enter", True, "white")
        self.window.blit(hint, hint.get_rect(center=(center_x, center_y + 30)))

    def render_game(self):
        self.level.render(self.playfield)
        self.player_group.draw(self.playfield)

        if self.state in ("paused", "focus_paused"):
            self.render_overlay("Pause")
        elif self.state == "won":
            self.render_overlay("Gewonnen! Neustart mit R")
        elif self.state == "game_over":
            self.render_overlay("Game Over! Neustart mit R")

        self.window.blit(self.playfield, (0, HUD_HEIGHT))
        self.render_hud()

    async def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            if self.state == "playing":
                self.update(self.dt)
            self.render()
            await asyncio.sleep(0)

        pygame.quit()
