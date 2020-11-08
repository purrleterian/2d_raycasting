import pygame
import math
from settings import *


vec = pygame.Vector2


def collide_rect2(one, two):
    return one.colliderect(two.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.gap = 4

        self.player_size = 25
        self._image = pygame.Surface(
            (self.player_size - self.gap, self.player_size - self.gap), pygame.SRCALPHA)

        self.image = self._image

        self.rect = self.image.get_rect(center=(x + self.gap, y + self.gap))
        self.collide_rect = pygame.Rect(0, 0, 25, 25)

        self.image.fill(PLAYER_COLOR)

        self.pos = vec(x + self.gap, y + self.gap)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.player_vel = 0.9

    def update(self):
        keys = pygame.key.get_pressed()
        self.acc = vec(0, 0)

        self.move(keys)
        if not keys[pygame.K_LSHIFT]:
            self.player_vel = 0.9

        else:
            self.player_vel = 0.3

        self.acc.x += self.vel.x * AIR_FRICTION
        self.acc.y += self.vel.y * AIR_FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.topleft = self.pos

        # ----- Wall Collisions ----- ###
        self.collide_rect.centerx = self.pos.x
        self.wall_collide("x")
        self.collide_rect.centery = self.pos.y
        self.wall_collide("y")
        self.rect.center = self.collide_rect.center
        # ----------------------------- #

        self.screen_boundary()
        # self.rotate()

    def move(self, keys):

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -self.player_vel
            self.direction = "left"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = +self.player_vel
            self.direction = "right"

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.acc.y = -self.player_vel
            self.direction = "down"

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.acc.y = +self.player_vel
            self.direction = "up"

    def screen_boundary(self):
        if self.rect.right > SCREEN_WIDTH:
            print("Right")

        elif self.rect.left < 0:
            print("Left")

        elif self.rect.bottom > SCREEN_HEIGHT:
            print("Bottom")

        elif self.rect.top < 0:
            print("Top")

    def rotate(self):

        # -------------------------ROTATION----------------------------- #
        # -------------------------------------------------------------- #

        mouse_x, mouse_y = pygame.mouse.get_pos()
        vec_x, vec_y = mouse_x - self.pos.x, mouse_y - self.pos.y

        angle = math.degrees(math.atan2(vec_x, vec_y))
        angle = (180 / math.pi) * -math.atan2(vec_y, vec_x)

        self.image = pygame.transform.rotate(self._image, (angle))
        self.rect = self.image.get_rect(center=self.rect.midbottom)

    def wall_collide(self, dir_):
        if dir_ == "x":
            hits = pygame.sprite.spritecollide(
                self.collide_rect, self.game.walls, False, collide_rect2)

            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - \
                        self.collide_rect.width / 2

                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + \
                        self.collide_rect.width / 2

                self.vel.x = 0
                self.collide_rect.centerx = self.pos.x

        if dir_ == "y":
            hits = pygame.sprite.spritecollide(
                self.collide_rect, self.game.walls, False, collide_rect2)

            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.collide_rect.width / 2

                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + \
                        self.collide_rect.width / 2

                self.vel.y = 0
                self.collide_rect.centery = self.pos.y


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.gap = 2

        self.image = pygame.Surface(
            (TILE_SIZE - self.gap, TILE_SIZE - self.gap))
        self.rect = self.image.get_rect(
            center=(x + self.gap / 2, y + self.gap / 2))
        self.image.fill(WALL_COLOR)
        self.pos = vec(x + self.gap / 2, y + self.gap / 2)

    def update(self):
        self.rect.topleft = self.pos


class Wall(Tile):
    def __init__(self, x, y):
        super().__init__(self, x, y)


class Portal(Tile):
    def __init__(self, x, y):
        super().__init__(self, x, y)
        self.image.fill((139, 109, 156))


class Ray(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.ray_dir = vec(1, 0)
        self.pos = vec(x, y)

    def update(self):

        self.rect.topleft = self.pos
        pygame.draw.line(self.image, RED, (0, 0),
                         (self.ray_dir.x*10, self.ray_dir.y*10))

    def cast(self, wall):
        x1 = wall.pos.x
        y1 = wall.pos.y
        x2 = wall.pos.x+wall.image.get_height()
        y2 = wall.pos.y+wall.image.get_height()
