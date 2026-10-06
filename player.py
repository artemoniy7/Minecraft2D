import math
import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.gravity = 0.5
        self.jump_force = -9
        self.on_ground = False
        self.facing_right = True
        self.walk_time = 0

        self.head = pygame.image.load('assets/player/head.png').convert_alpha()
        self.body = pygame.image.load('assets/player/body.png').convert_alpha()
        self.arm = pygame.image.load('assets/player/arm.png').convert_alpha()
        self.leg = pygame.image.load('assets/player/leg.png').convert_alpha()

    def update(self, keys, mouse_x):
        moving = False
        self.vx = 0

        if keys[pygame.K_a]:
            self.vx = -self.speed
            moving = True
        if keys[pygame.K_d]:
            self.vx = self.speed
            moving = True

        self.facing_right = mouse_x >= 640

        if moving:
            self.walk_time += 0.15

        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

        ground_y = 360 - 64
        if self.y > ground_y:
            self.y = ground_y
            self.vy = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_force
            self.on_ground = False

    def draw(self, screen):
        swing = math.sin(self.walk_time) * 20
        flip = not self.facing_right

        leg1 = pygame.transform.flip(pygame.transform.rotate(self.leg, swing), flip, False)
        leg2 = pygame.transform.flip(pygame.transform.rotate(self.leg, -swing), flip, False)
        arm1 = pygame.transform.flip(pygame.transform.rotate(self.arm, -swing), flip, False)
        arm2 = pygame.transform.flip(pygame.transform.rotate(self.arm, swing), flip, False)

        body = pygame.transform.flip(self.body, flip, False)
        head = pygame.transform.flip(self.head, flip, False)

        screen.blit(leg1, (self.x - 10, self.y + 32))
        screen.blit(leg2, (self.x + 10, self.y + 32))
        screen.blit(arm1, (self.x - 12, self.y + 5))
        screen.blit(body, (self.x, self.y))
        screen.blit(arm2, (self.x + 12, self.y + 5))
        screen.blit(head, (self.x, self.y - 28))