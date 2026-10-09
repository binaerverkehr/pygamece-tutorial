import pygame


class Player:
    def __init__(self, x: float, y: float, radius, color):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.speed = 600
        self.color = color
        self.keys = 0

    def pickup_key(self):
        self.keys += 1

    def use_key(self):
        if self.keys:
            self.keys -= 1
            return True

    def overlaps_rect(self, rect):
        nearest = pygame.Vector2(
            pygame.math.clamp(self.pos.x, rect.left, rect.right),
            pygame.math.clamp(self.pos.y, rect.top, rect.bottom),
        )
        return self.pos.distance_squared_to(nearest) < self.radius**2

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.pos.x, self.pos.y), self.radius)
