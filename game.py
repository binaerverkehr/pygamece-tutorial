import pygame

TILE_SIZE = 60
PLAYER_RADIUS = 20
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

level1 = [
    "################",
    "#P     #       #",
    "# #### # ##### #",
    "#    #   #     #",
    "#### ##### ### #",
    "#          #  G#",
    "################",
]

level2 = [
    "################",
    "#G     #       #",
    "# #### # ## ####",
    "# ####    # ##P#",
    "# ######### ## #",
    "#     #        #",
    "################",
]

level3 = [
    "################",
    "#P####    ####G#",
    "# #### ## #### #",
    "#      ##      #",
    "################",
]


class Player:
    def __init__(self, x: float, y: float, radius, color):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.speed = 600
        self.color = color

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

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


class Level:
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.walls = []
        self.goal = None
        self.player_start_x = 0
        self.player_start_y = 0

        for row_index, row in enumerate(self.layout):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if char == "#":
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == "P":
                    self.player_start_x = x + TILE_SIZE / 2
                    self.player_start_y = y + TILE_SIZE / 2
                elif char == "G":
                    self.goal = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    @property
    def cols(self):
        return len(self.layout[0])

    @property
    def rows(self):
        return len(self.layout)

    def render(self, surface):
        for rect in self.walls:
            pygame.draw.rect(surface, "grey", rect)

        if self.goal is not None:
            pygame.draw.rect(surface, "green", self.goal)


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        self.levels = [Level(level1), Level(level2), Level(level3)]
        self.level_index = 0
        self.level: Level = self.levels[self.level_index]

        self.load_level(self.level_index)

        width = self.level.cols * TILE_SIZE
        height = self.level.rows * TILE_SIZE
        self.window = pygame.display.set_mode((width, height))

        player_x = self.level.player_start_x
        player_y = self.level.player_start_y
        self.player = Player(player_x, player_y, PLAYER_RADIUS, "blue")

        self.won = False
        font = pygame.font.Font(None, 72)
        self.win_text = font.render("Gewonnen!", True, "black")

    def move_player(self, dt):
        player = self.player
        distance = player.speed * dt

        dx = 0
        dy = 0

        if self.keys[pygame.K_w]:
            dy -= distance
        if self.keys[pygame.K_s]:
            dy += distance
        if self.keys[pygame.K_a]:
            dx -= distance
        if self.keys[pygame.K_d]:
            dx += distance

        steps = int(distance) + 1
        step_x = dx / steps
        step_y = dy / steps

        for _ in range(steps):
            previous_x = player.x
            player.x += step_x

            if player.x - player.radius < 0:
                player.x = player.radius
            if player.x + player.radius > WINDOW_WIDTH:
                player.x = WINDOW_WIDTH - player.radius

            for wall in self.level.walls:
                if player.overlaps_rect(wall):
                    player.x = previous_x
                    break

            previous_y = player.y
            player.y += step_y

            if player.y - player.radius < 0:
                player.y = player.radius
            if player.y + player.radius > WINDOW_HEIGHT:
                player.y = WINDOW_HEIGHT - player.radius

            for wall in self.level.walls:
                if player.overlaps_rect(wall):
                    player.y = previous_y
                    break

    def load_level(self, index):
        self.level = self.levels[index]
        # Fenstergröße an Levelgröße anpassen
        width = self.level.cols * TILE_SIZE
        height = self.level.rows * TILE_SIZE
        self.window = pygame.display.set_mode((width, height))

        # Entities
        self.player = Player(
            self.level.player_start_x,
            self.level.player_start_y,
            PLAYER_RADIUS,
            "blue",
        )

    def handle_events(self):
        # Fenster-Ereignisse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        # Tastatur-Ereignisse
        self.keys = pygame.key.get_pressed()
        """
        Spiel-Ereignisse
        """
        # Spieler erreicht Level-Ziel
        if not self.won and self.player.overlaps_rect(self.level.goal):
            # Wenn letztes Level erreicht, Sieg ansonsten nächstes Level
            if self.level_index + 1 >= len(self.levels):
                self.won = True
            else:
                self.level_index += 1
                self.load_level(self.level_index)

    def update(self, dt):
        self.move_player(dt)

    def render(self):
        # Hintergrund zeichnen
        self.window.fill("white")

        self.level.render(self.window)
        self.player.render(self.window)

        if self.won:
            text_rect = self.win_text.get_rect(center=self.window.get_rect().center)
            self.window.blit(self.win_text, text_rect)

        # Display aktualisieren
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.update(self.dt)
            self.render()

        pygame.quit()


Game().run()
