import pygame

from constants import TILE_SIZE


class Level:
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.walls = []
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


test_levels = [
    Level(
        [
            "################",
            "#P     #       #",
            "# #### # ##### #",
            "#    #   #     #",
            "#### ##### ### #",
            "#          #  G#",
            "################",
        ]
    ),
    Level(
        [
            "################",
            "#G     #       #",
            "# #### # ## ####",
            "# ####    # ##P#",
            "# ######### ## #",
            "#     #        #",
            "################",
        ]
    ),
    Level(
        [
            "################",
            "#P####    ####G#",
            "# #### ## #### #",
            "#      ##      #",
            "################",
        ]
    ),
]
