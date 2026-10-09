import pygame


class Enemy:
    def __init__(self, x: float, y: float, radius, color):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.color = color

    def render(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
