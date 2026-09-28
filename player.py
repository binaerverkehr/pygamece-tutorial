import pygame


class Player:
    def __init__(self, x: float, y: float, radius, color):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.speed = 600
        self.color = color
        self.inventory = []

    def overlaps_rect(self, rect):
        nearest_x = self.x
        if self.x < rect.left:
            nearest_x = rect.left
        elif self.x > rect.right:
            nearest_x = rect.right

        nearest_y = self.y
        if self.y < rect.top:
            nearest_y = rect.top
        elif self.y > rect.bottom:
            nearest_y = rect.bottom

        dx = self.x - nearest_x
        dy = self.y - nearest_y
        distance_squared = dx * dx + dy * dy
        return distance_squared < self.radius * self.radius

    def take(self, item):
        self.inventory.append(item)

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
