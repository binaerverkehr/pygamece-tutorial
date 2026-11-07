from character import Character


class Player(Character):
    def __init__(self, radius, image):
        super().__init__(radius, image)
        self.speed = 600
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
