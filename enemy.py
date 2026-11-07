import pygame

from character import Character

ENEMY_DIRECTIONS = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


class Enemy(Character):
    def __init__(self, x: float, y: float, radius, image, direction):
        super().__init__(radius, image)
        self.pos.update(x, y)
        self.direction = pygame.Vector2(direction)
        self.speed = 200

    def update(self, dt, obstacles):
        previous_pos = self.pos.copy()
        self.pos += self.direction * self.speed * dt

        for obstacle in obstacles:
            if self.overlaps_rect(obstacle.rect):
                self.pos = previous_pos
                self.direction = -self.direction
                break
