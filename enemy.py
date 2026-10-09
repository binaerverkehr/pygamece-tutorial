import pygame


class Enemy:
    def __init__(self, x: float, y: float, radius, color):
        self.pos = pygame.Vector2(x, y)
        self.direction = pygame.Vector2(1, 0)
        self.radius = radius
        self.speed = 200
        self.color = color

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
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
