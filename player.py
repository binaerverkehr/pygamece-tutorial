import pygame


class Player:
    def __init__(self, radius, image):
        self.pos = pygame.Vector2()
        self.radius = radius
        self.speed = 600
        self.image = image
        self.keys = 0
        self.lives = 3

    def respawn(self, x: float, y: float):
        self.pos.update(x, y)
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
        surface.blit(self.image, self.pos)
