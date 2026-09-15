import pygame


class Player:
    def __init__(self, x: float, y: float, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height

    @property
    def rect(self):
        return pygame.Rect((self.x, self.y), (self.width, self.height))
