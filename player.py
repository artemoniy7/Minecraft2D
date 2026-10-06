import math
import pygame


class Player:
    BLOCK_SIZE = 64
    SCALE = 1.75

    GAP_HEAD_BODY = 1
    GAP_BODY_LEG  = 1
    GAP_ARM_BODY  = 0
    SIDE_OFFSET   = 1

    PIVOT_TOP_OFFSET = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.gravity = 0.5
        self.jump_force = -12
        self.on_ground = False
        self.facing_right = True
        self.walk_time = 0

        head_raw = pygame.image.load('assets/player/head.png').convert_alpha()
        body_raw = pygame.image.load('assets/player/body.png').convert_alpha()
        arm_raw  = pygame.image.load('assets/player/arm.png').convert_alpha()
        leg_raw  = pygame.image.load('assets/player/leg.png').convert_alpha()

        raw_total_height = (
            head_raw.get_height()
            + body_raw.get_height()
            + leg_raw.get_height()
        )

        target_height = self.BLOCK_SIZE * self.SCALE
        scale = target_height / raw_total_height

        self.head = self._scale(head_raw, scale)
        self.body = self._scale(body_raw, scale)
        self.arm  = self._scale(arm_raw,  scale)
        self.leg  = self._scale(leg_raw,  scale)

        self.total_height = (
            self.head.get_height()
            + self.GAP_HEAD_BODY
            + self.body.get_height()
            + self.GAP_BODY_LEG
            + self.leg.get_height()
        )

    def _scale(self, image, scale):
        w = max(1, round(image.get_width() * scale))
        h = max(1, round(image.get_height() * scale))
        return pygame.transform.scale(image, (w, h))

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

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_force
            self.on_ground = False

    def _blit_pivoted(self, screen, image, angle, anchor_x, anchor_y, flip):
        if flip:
            image = pygame.transform.flip(image, True, False)

        pivot = pygame.math.Vector2(image.get_width() / 2, self.PIVOT_TOP_OFFSET)
        rotated = pygame.transform.rotate(image, angle)

        rel = pivot - pygame.math.Vector2(image.get_width() / 2, image.get_height() / 2)
        rel.rotate_ip(-angle)

        rotated_center = pygame.math.Vector2(rotated.get_width() / 2, rotated.get_height() / 2)
        pivot_in_rotated = rotated_center + rel

        blit_x = anchor_x - pivot_in_rotated.x
        blit_y = anchor_y - pivot_in_rotated.y

        screen.blit(rotated, (blit_x, blit_y))

    def draw(self, screen):
        swing = math.sin(self.walk_time) * 18
        flip = not self.facing_right

        body = pygame.transform.flip(self.body, flip, False)
        head = pygame.transform.flip(self.head, flip, False)

        center_x = int(self.x) + self.body.get_width() // 2

        head_y = int(self.y)
        body_y = head_y + head.get_height() + self.GAP_HEAD_BODY
        arm_y  = body_y + self.GAP_ARM_BODY
        leg_y  = body_y + body.get_height() + self.GAP_BODY_LEG

        self._blit_pivoted(screen, self.leg, -swing,
                           center_x - self.SIDE_OFFSET, leg_y, flip)
        self._blit_pivoted(screen, self.leg,  swing,
                           center_x + self.SIDE_OFFSET, leg_y, flip)

        self._blit_pivoted(screen, self.arm, -swing,
                           center_x - self.SIDE_OFFSET, arm_y, flip)

        screen.blit(body, (center_x - body.get_width() // 2, body_y))

        self._blit_pivoted(screen, self.arm, swing,
                           center_x + self.SIDE_OFFSET, arm_y, flip)

        screen.blit(head, (center_x - head.get_width() // 2, head_y))