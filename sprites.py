import pygame
import math
from settings import *
from rooms import level

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
        self.level_position = [1, 1]

        self.projectiles = pygame.sprite.Group()
        self.projectile_speed = 5

        self.direction = "up"

    def update(self):
        keys = pygame.key.get_pressed()
        self.acc = vec(0, 0)

        self.move(keys)
        self.screen_boundary()
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
            self.direction = "up"

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.acc.y = +self.player_vel
            self.direction = "down"

        # Diagonal
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.direction = "topleft"

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.direction = "topright"

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.direction = "bottomleft"

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.direction = "bottomright"

    def screen_boundary(self):
        if self.rect.left > SCREEN_WIDTH - self.player_size // 2:
            self.pos.x = self.player_size
            self.level_position[0] += 1
            self.game.load_room(level[tuple(self.level_position)])

        elif self.rect.right < self.player_size//2:
            self.pos.x = SCREEN_WIDTH - self.player_size
            self.level_position[0] -= 1
            self.game.load_room(level[tuple(self.level_position)])

        elif self.rect.top > SCREEN_HEIGHT - self.player_size//2:
            self.pos.y = self.player_size
            self.level_position[1] += 1
            self.game.load_room(level[tuple(self.level_position)])

        elif self.rect.bottom < self.player_size//2:
            self.pos.y = SCREEN_HEIGHT - self.player_size
            self.level_position[1] -= 1
            self.game.load_room(level[tuple(self.level_position)])

    def rotate(self):

        # -------------------------ROTATION----------------------------- #
        # -------------------------------------------------------------- #

        mouse_x, mouse_y = pygame.mouse.get_pos()
        vec_x, vec_y = mouse_x - self.pos.x, mouse_y - self.pos.y

        angle = math.degrees(math.atan2(vec_x, vec_y))
        angle = (180 / math.pi) * -math.atan2(vec_y, vec_x)

        self.image = pygame.transform.rotate(self._image, (angle))
        self.rect = self.image.get_rect(center=self.rect.midbottom)

    def shoot(self):
        proj = Projectile(self)

        self.game.all_sprites.add(proj)
        self.projectiles.add(proj)

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


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player

        self.x, self.y = self.player.rect.center

        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.image.fill(PLAYER_COLOR)

        self.pos = vec(self.x, self.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.direction = self.player.direction

        self.projectile_speed = 3

    def update(self):
        print(self.direction)
        if self.direction == "right":
            self.acc = vec(self.projectile_speed, 0)

        elif self.direction == "left":
            self.acc = vec(-self.projectile_speed, 0)

        elif self.direction == "up":
            self.acc = vec(0, -self.projectile_speed)

        elif self.direction == "down":
            self.acc = vec(0, self.projectile_speed)

        # Diagonal

        if self.direction == "topright":
            self.acc = vec(self.projectile_speed, -self.projectile_speed)

        elif self.direction == "topleft":
            self.acc = vec(-self.projectile_speed, -self.projectile_speed)

        elif self.direction == "bottomright":
            self.acc = vec(self.projectile_speed, self.projectile_speed)

        elif self.direction == "bottomleft":
            self.acc = vec(-self.projectile_speed, self.projectile_speed)

        self.acc.x += self.vel.x * AIR_FRICTION
        self.acc.y += self.vel.y * AIR_FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos


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
