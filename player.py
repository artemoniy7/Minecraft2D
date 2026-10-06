import math
import pygame


class Player:
    SCALE = 1.75

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.gravity = 0.5
        self.jump_force = -10
        self.on_ground = False
        self.facing_right = True
        self.walk_time = 0

        self.head = self._load_scaled('assets/player/head.png')
        self.body = self._load_scaled('assets/player/body.png')
        self.arm = self._load_scaled('assets/player/arm.png')
        self.leg = self._load_scaled('assets/player/leg.png')

    def _load_scaled(self, path):
        image = pygame.image.load(path).convert_alpha()
        width = round(image.get_width() * self.SCALE)
        height = round(image.get_height() * self.SCALE)
        return pygame.transform.scale(image, (width, height))

    def update(self, keys, mouse_x):
        moving = False
        self.vx = 0

        if keys[pygame.K_a]:
            self.vx = -self.speed
            moving = True
        if keys[pygame.K_d]:
            self.vx = self.speed
            moving = True

        self.facing_right = mouse_x >= self.x

        if moving:
            self.walk_time += 0.2

        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

        ground_y = 360 - int(24 * self.SCALE)
        if self.y > ground_y:
            self.y = ground_y
            self.vy = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_force
            self.on_ground = False

    def draw(self, screen):
        swing = math.sin(self.walk_time) * 18
        flip = not self.facing_right

        back_leg = pygame.transform.flip(pygame.transform.rotate(self.leg, -swing), flip, False)
        front_leg = pygame.transform.flip(pygame.transform.rotate(self.leg, swing), flip, False)

        back_arm = pygame.transform.flip(pygame.transform.rotate(self.arm, -swing), flip, False)
        front_arm = pygame.transform.flip(pygame.transform.rotate(self.arm, swing), flip, False)

        body = pygame.transform.flip(self.body, flip, False)
        head = pygame.transform.flip(self.head, flip, False)

        px = int(self.x)
        py = int(self.y)

        screen.blit(back_leg, (px - round(2 * self.SCALE), py + round(12 * self.SCALE)))
        screen.blit(front_leg, (px + round(2 * self.SCALE), py + round(12 * self.SCALE)))

        screen.blit(back_arm, (px - round(4 * self.SCALE), py))
        screen.blit(body, (px, py))
        screen.blit(front_arm, (px + round(4 * self.SCALE), py))

        screen.blit(head, (px, py - round(4 * self.SCALE)))