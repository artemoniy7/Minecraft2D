import pygame
from block_registry import BlockRegistry
from player import Player

pygame.init()
WIDTH, HEIGHT = 1280, 720
FPS = 60
BLOCK_SIZE = 64

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Параметры мира ---
WORLD_HEIGHT = 60
GROUND_LEVEL = 30
DIRT_DEPTH   = 4
WORLD_WIDTH  = WIDTH // BLOCK_SIZE + 2

# --- Реестр блоков ---
registry = BlockRegistry()
registry.load()


def load_texture(internal_name):
    block = registry.get(internal_name)
    if block is None:
        raise ValueError(f"Блок '{internal_name}' не найден в blocks.json")
    img = pygame.image.load(f'assets/blocks/{block.texture}').convert_alpha()
    return pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))


TEXTURES = {
    'grass': load_texture('grass'),
    'dirt':  load_texture('dirt'),
    'stone': load_texture('stone'),
}

# --- Генерация мира ---
# world[y][x] = internal_name блока или None
world = []
for y in range(WORLD_HEIGHT):
    row = []
    for x in range(WORLD_WIDTH):
        if y < GROUND_LEVEL:
            row.append(None)
        elif y == GROUND_LEVEL:
            row.append('grass')
        elif y <= GROUND_LEVEL + DIRT_DEPTH:
            row.append('dirt')
        else:
            row.append('stone')
    world.append(row)

# --- Таблица коллизий ---
# collision[y][x] = True, если блок твёрдый
collision = []
for y in range(WORLD_HEIGHT):
    row = []
    for x in range(WORLD_WIDTH):
        name = world[y][x]
        if name is None:
            row.append(False)
        else:
            block = registry.get(name)
            row.append(bool(block and block.has_collision))
    collision.append(row)

WORLD_PIXEL_WIDTH  = WORLD_WIDTH  * BLOCK_SIZE
WORLD_PIXEL_HEIGHT = WORLD_HEIGHT * BLOCK_SIZE

# --- Игрок ---
SURFACE_Y = GROUND_LEVEL * BLOCK_SIZE
player = Player(BLOCK_SIZE * 4, SURFACE_Y - 300)

camera_x = 0
camera_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()

    keys = pygame.key.get_pressed()

    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2
    camera_x = max(0, min(camera_x, WORLD_PIXEL_WIDTH  - WIDTH))
    camera_y = max(0, min(camera_y, WORLD_PIXEL_HEIGHT - HEIGHT))

    mouse_screen_x, _ = pygame.mouse.get_pos()
    mouse_world_x = mouse_screen_x + camera_x

    player.update(keys, mouse_world_x, collision, BLOCK_SIZE)

    screen.fill((135, 206, 235))

    start_x = max(0, int(camera_x) // BLOCK_SIZE)
    end_x   = min(WORLD_WIDTH,  (int(camera_x) + WIDTH)  // BLOCK_SIZE + 1)
    start_y = max(0, int(camera_y) // BLOCK_SIZE)
    end_y   = min(WORLD_HEIGHT, (int(camera_y) + HEIGHT) // BLOCK_SIZE + 1)

    for y in range(start_y, end_y):
        row = world[y]
        for x in range(start_x, end_x):
            name = row[x]
            if name is None:
                continue
            screen_x = x * BLOCK_SIZE - camera_x
            screen_y = y * BLOCK_SIZE - camera_y
            screen.blit(TEXTURES[name], (screen_x, screen_y))

    # Игрок с учётом камеры
    old_x, old_y = player.x, player.y
    player.x -= camera_x
    player.y -= camera_y
    player.draw(screen)
    player.x, player.y = old_x, old_y

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()