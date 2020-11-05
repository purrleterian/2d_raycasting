import pygame
import math
from settings import *


vec = pygame.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.player_size = 25
        self._image = pygame.Surface(
            (self.player_size, self.player_size), pygame.SRCALPHA)

        self.image = self._image

        self.rect = self.image.get_rect()
        self.image.fill(WHITE)

        self.pos = vec(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.player_vel = 0.9

    def update(self):
        keys = pygame.key.get_pressed()
        self.acc = vec(0, 0)

        if not keys[pygame.K_LSHIFT]:
            self.player_vel = 0.9
            self.move(keys)

        else:
            self.move(keys)
            self.player_vel = 0.3

        self.acc.x += self.vel.x * AIR_FRICTION
        self.acc.y += self.vel.y * AIR_FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

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

    def rotate(self):

        # -------------------------ROTATION----------------------------- #
        # -------------------------------------------------------------- #

        mouse_x, mouse_y = pygame.mouse.get_pos()
        vec_x, vec_y = mouse_x - self.pos.x, mouse_y - self.pos.y

        angle = math.degrees(math.atan2(vec_x, vec_y))
        angle = (180 / math.pi) * -math.atan2(vec_y, vec_x)

        self.image = pygame.transform.rotate(self._image, angle)
        self.rect = self.image.get_rect(center=self.rect.midbottom)


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.image = pygame.Surface((WALL_SIZE, WALL_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image.fill(WHITE)

        self.pos = vec(x, y)

    def update(self):
        pass
        # self.rect = self.pos
