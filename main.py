import pygame

from block_registry import BlockRegistry

pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 60
BLOCK_SIZE = 64
CAMERA_SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft 2D")
clock = pygame.time.Clock()

registry = BlockRegistry()
registry.load()

stone = registry.get("stone")

textures = {}
if stone:
    texture = pygame.image.load(f"assets/blocks/{stone.texture}").convert_alpha()
    textures[stone.internal_name] = pygame.transform.scale(
        texture,
        (BLOCK_SIZE, BLOCK_SIZE),
    )

camera_x = 0
camera_y = 0

platform = []
for x in range(15):
    platform.append({
        "block": stone,
        "x": x * BLOCK_SIZE,
        "y": 0,
    })

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

    for block_data in platform:
        block = block_data["block"]
        texture = textures.get(block.internal_name)

        if texture is None:
            continue

        screen.blit(
            texture,
            (
                block_data["x"] - camera_x,
                HEIGHT // 2 + block_data["y"] - camera_y,
            ),
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
