import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, radius, image):
        super().__init__()
        self.pos = pygame.Vector2()
        self.radius = radius
        self.image = image

    def overlaps_rect(self, rect):
        nearest = pygame.Vector2(
            pygame.math.clamp(self.pos.x, rect.left, rect.right),
            pygame.math.clamp(self.pos.y, rect.top, rect.bottom),
        )
        return self.pos.distance_squared_to(nearest) < self.radius**2

    @property
    def rect(self):
        return self.image.get_rect(center=self.pos)
