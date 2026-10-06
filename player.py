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
        self.jump_force = -10
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

        self.facing_right = mouse_x >= self.x

        if moving:
            self.walk_time += 0.2

        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy

        ground_y = 360 - 24
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

        # Ноги: задняя -> передняя
        screen.blit(back_leg, (px - 2, py + 12))
        screen.blit(front_leg, (px + 2, py + 12))

        # Верхняя часть: рука -> тело -> рука
        screen.blit(back_arm, (px - 4, py))
        screen.blit(body, (px, py))
        screen.blit(front_arm, (px + 4, py))

        # Голова
        screen.blit(head, (px, py - 4))