import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 60
BLOCK_SIZE = 64
CAMERA_SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft 2D")
clock = pygame.time.Clock()

stone_texture = pygame.image.load("assets/blocks/stone.png").convert_alpha()
stone_texture = pygame.transform.scale(stone_texture, (BLOCK_SIZE, BLOCK_SIZE))

camera_x = 0
camera_y = 0

platform = []
for x in range(15):
    platform.append((x * BLOCK_SIZE, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        camera_x -= CAMERA_SPEED
    if keys[pygame.K_d]:
        camera_x += CAMERA_SPEED
    if keys[pygame.K_w]:
        camera_y -= CAMERA_SPEED
    if keys[pygame.K_s]:
        camera_y += CAMERA_SPEED

    screen.fill((135, 206, 235))

    for block_x, block_y in platform:
        screen.blit(
            stone_texture,
            (
                block_x - camera_x,
                HEIGHT // 2 + block_y - camera_y,
            ),
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
