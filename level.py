import pygame

from constants import ENEMY_RADIUS, TILE_SIZE
from enemy import Enemy


class Level:
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.walls = []
        self.keys = []
        self.doors = []
        self.enemies = []
        self.goal = None
        self.player_start_x = 0
        self.player_start_y = 0

        for row_index, row in enumerate(self.layout):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if char == "#":
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == "P":
                    self.player_start_x = x + TILE_SIZE / 2
                    self.player_start_y = y + TILE_SIZE / 2
                elif char == "G":
                    self.goal = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                elif char == "K":
                    w = TILE_SIZE * 0.2
                    h = TILE_SIZE * 0.2
                    key_rect = pygame.Rect(x + TILE_SIZE / 2 - w / 2, y + TILE_SIZE / 2 - h / 2, w, h)
                    self.keys.append(key_rect)
                elif char == "D":
                    door_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.doors.append(door_rect)
                elif char == "E":
                    enemy_x = x + TILE_SIZE / 2
                    enemy_y = y + TILE_SIZE / 2
                    enemy_rect = Enemy(enemy_x, enemy_y, ENEMY_RADIUS, "red")
                    self.enemies.append(enemy_rect)

    @property
    def cols(self):
        return len(self.layout[0])

    @property
    def rows(self):
        return len(self.layout)

    def render(self, surface):
        for rect in self.walls:
            pygame.draw.rect(surface, "grey", rect)

        if self.goal is not None:
            pygame.draw.rect(surface, "green", self.goal)

        for door in self.doors:
            pygame.draw.rect(surface, "brown", door)

        for key in self.keys:
            pygame.draw.rect(surface, "yellow", key)

        for enemy in self.enemies:
            enemy.render(surface)


LAYOUTS = [
    [
        "################",
        "#P     #       #",
        "# #### # ##### #",
        "#    #   #  E  #",
        "#### #########D#",
        "#         K#G  #",
        "################",
    ],
    [
        "################",
        "#      #      K#",
        "#D##K# #D## ####",
        "#D##K#    # ##P#",
        "# #########D## #",
        "#    G#K       #",
        "################",
    ],
    [
        "################",
        "#P#K##      K#G#",
        "# # ##D##D#### #",
        "#      ##      #",
        "################",
    ],
]
