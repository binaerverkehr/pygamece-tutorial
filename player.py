class Player:
    def __init__(self, x: float, y: float, radius):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius

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
