import pygame

ENEMY_DIRECTIONS = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


class Enemy:
    def __init__(self, x: float, y: float, radius, image, direction):
        self.pos = pygame.Vector2(x, y)
        self.direction = pygame.Vector2(direction)
        self.radius = radius
        self.speed = 200
        self.image = image

    def overlaps_rect(self, rect):
        nearest = pygame.Vector2(
            pygame.math.clamp(self.pos.x, rect.left, rect.right),
            pygame.math.clamp(self.pos.y, rect.top, rect.bottom),
        )
        return self.pos.distance_squared_to(nearest) < self.radius**2

    def update(self, dt, obstacles):
        previous_pos = self.pos.copy()
        self.pos += self.direction * self.speed * dt

        for obstacle in obstacles:
            if self.overlaps_rect(obstacle):
                self.pos = previous_pos
                self.direction = -self.direction
                break

    def render(self, surface):
        surface.blit(self.image, self.image.get_rect(center=self.pos))
