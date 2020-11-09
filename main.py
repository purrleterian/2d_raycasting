import pygame
from pygame import mouse
from settings import *
from sprites import *
from rooms import level


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

    def load_room(self, room):
        # Clear the room before loading a new room
        self.walls.empty()
        self.tiles.empty()
        for e in self.all_sprites:
            if isinstance(e, Tile):
                e.kill()

        for y, column in enumerate(room.layout):
            for x, tile in enumerate(column):
                if tile == 1:
                    wall = Wall(x*TILE_SIZE, y*TILE_SIZE)
                    self.tiles.add(wall)
                    self.walls.add(wall)

        for tile in self.tiles:
            self.all_sprites.add(tile)

    def new(self):
        # Add Sprite Groups below
        self.all_sprites = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        # Add Sprites below
        self.load_room(level[(1, 1)])

        self.player = Player(self, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot()

    def update(self):
        self.all_sprites.update()
        self.tiles.update()

        for proj in self.player.projectiles:
            wall_hits = pygame.sprite.spritecollide(proj, self.tiles, False)
            if wall_hits:
                proj.kill()

            if proj.pos.x > SCREEN_WIDTH or proj.pos.x < 0 or proj.pos.y > SCREEN_HEIGHT or proj.pos.y < 0:
                proj.kill()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.display.set_caption(
            f"Dungeon Crawler | {self.clock.get_fps():.2F} FPS")

        self.all_sprites.draw(self.screen)
        pygame.display.flip()


game = Game()
while game.running:
    game.new()

pygame.quit()
quit()
