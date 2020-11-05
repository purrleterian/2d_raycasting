import pygame
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # Initialize audio settings
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # Create a screen and a clock
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.running = True
        # Load assets like textures and audio
        self.load_data()

    def load_data(self):
        pass

    def new(self):
        # Add Sprite Groups below
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        # Add Sprites below
        self.player = Player(self)
        for y, column in enumerate(WORLD_MAP):
            for x, space in enumerate(column):
                if space == 1:
                    wall = Wall(self, x*WALL_SIZE, y*WALL_SIZE)
                    self.walls.add(wall)

        for wall in self.walls:
            self.all_sprites.add(wall)

        self.all_sprites.add(self.player)
        # ----------------- #
        # ------ RUN ------ #
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()

            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False

    def update(self):
        self.all_sprites.update()
        self.walls.update()

        for wall in self.walls:
            if wall.rect.colliderect(self.player.rect):
                print("Collision")

    def draw(self):
        self.screen.fill(BLACK)
        pygame.display.set_caption(f"{self.clock.get_fps():.2F} FPS")

        self.all_sprites.draw(self.screen)
        pygame.display.flip()


game = Game()
while game.running:
    game.new()

pygame.quit()
quit()
