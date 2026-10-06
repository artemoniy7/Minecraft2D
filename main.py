import math
import random

import pygame

from block_registry import BlockRegistry
from player import Player


pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
BLOCK_SIZE = 64

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft 2D")
clock = pygame.time.Clock()


# --- Реестр блоков ---
registry = BlockRegistry()
registry.load()


def load_texture(internal_name):
    block = registry.get(internal_name)
    if block is None:
        raise ValueError(f"Блок '{internal_name}' не найден в blocks.json")
    img = pygame.image.load(f"assets/blocks/{block.texture}").convert_alpha()
    return pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))


TEXTURES = {
    "grass": load_texture("grass"),
    "dirt": load_texture("dirt"),
    "stone": load_texture("stone"),
}


class World:
    """Бесконечный по X мир с чанками и выгрузкой далёких чанков."""

    CHUNK_SIZE = 16
    WORLD_HEIGHT = 80
    RENDER_DISTANCE = 10
    UNLOAD_DISTANCE = RENDER_DISTANCE + 2
    SEED = 271828

    def __init__(self):
        self.loaded_chunks = set()
        self.blocks = {}

    @staticmethod
    def _chunk_x(x):
        return math.floor(x / World.CHUNK_SIZE)

    def _surface_height(self, x):
        # Несколько частот дают более естественные холмы, а детерминированный
        # шум добавляет небольшую неровность, сохраняя один и тот же мир.
        low = math.sin(x * 0.035) * 5.0
        medium = math.sin(x * 0.09 + 1.7) * 2.5
        detail = math.sin(x * 0.22 + 4.0) * 0.8

        rng = random.Random(self.SEED + x * 1009)
        jitter = rng.uniform(-1.2, 1.2)

        return max(5, min(self.WORLD_HEIGHT - 8, round(27 + low + medium + detail + jitter)))

    def _generate_chunk(self, chunk_x):
        if chunk_x in self.loaded_chunks:
            return

        start_x = chunk_x * self.CHUNK_SIZE
        end_x = start_x + self.CHUNK_SIZE

        for x in range(start_x, end_x):
            surface = self._surface_height(x)

            for y in range(surface, self.WORLD_HEIGHT):
                if y == surface:
                    name = "grass"
                elif y < surface + 4:
                    name = "dirt"
                else:
                    name = "stone"

                self.blocks[(x, y)] = name

        self.loaded_chunks.add(chunk_x)

    def update_streaming(self, player_x):
        center_chunk = self._chunk_x(math.floor(player_x / BLOCK_SIZE))

        for chunk_x in range(
            center_chunk - self.RENDER_DISTANCE,
            center_chunk + self.RENDER_DISTANCE + 1,
        ):
            self._generate_chunk(chunk_x)

        keep_min = center_chunk - self.UNLOAD_DISTANCE
        keep_max = center_chunk + self.UNLOAD_DISTANCE

        for chunk_x in tuple(self.loaded_chunks):
            if keep_min <= chunk_x <= keep_max:
                continue

            start_x = chunk_x * self.CHUNK_SIZE
            end_x = start_x + self.CHUNK_SIZE

            for x in range(start_x, end_x):
                for y in range(self.WORLD_HEIGHT):
                    self.blocks.pop((x, y), None)

            self.loaded_chunks.remove(chunk_x)

    def get_block(self, x, y):
        if y < 0:
            return None
        if y >= self.WORLD_HEIGHT:
            return "stone"
        return self.blocks.get((x, y))

    def is_solid(self, x, y):
        name = self.get_block(x, y)
        if name is None:
            return False

        block = registry.get(name)
        return bool(block and block.has_collision)

    def surface_y(self, x):
        return self._surface_height(x) * BLOCK_SIZE


world = World()

# Загружаем стартовую область до появления игрока.
world.update_streaming(0)
spawn_x = 4 * BLOCK_SIZE
spawn_surface_y = world.surface_y(4)
player = Player(spawn_x, spawn_surface_y - 300)


# --- Плавная камера ---
camera = pygame.Vector2(
    player.x + player.body.get_width() / 2 - WIDTH / 2,
    player.y + player.total_height / 2 - HEIGHT / 2,
)
CAMERA_FOLLOW_SPEED = 9.0


def update_camera(dt):
    target_x = player.x + player.body.get_width() / 2 - WIDTH / 2
    target_y = player.y + player.total_height / 2 - HEIGHT / 2

    # Экспоненциальное сглаживание не зависит от FPS.
    blend = 1.0 - math.exp(-CAMERA_FOLLOW_SPEED * dt)
    camera.x += (target_x - camera.x) * blend
    camera.y += (target_y - camera.y) * blend

    camera.y = max(
        0.0,
        min(camera.y, world.WORLD_HEIGHT * BLOCK_SIZE - HEIGHT),
    )


running = True

while running:
    dt = min(clock.tick(FPS) / 1000.0, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()

    # Чанки появляются впереди игрока, а далёкие выгружаются из памяти.
    world.update_streaming(player.x)

    mouse_screen_x, _ = pygame.mouse.get_pos()
    mouse_world_x = mouse_screen_x + camera.x

    keys = pygame.key.get_pressed()
    player.update(keys, mouse_world_x, world, BLOCK_SIZE)
    world.update_streaming(player.x)
    update_camera(dt)

    screen.fill((135, 206, 235))

    start_x = math.floor(camera.x / BLOCK_SIZE) - 1
    end_x = math.floor((camera.x + WIDTH) / BLOCK_SIZE) + 2
    start_y = max(0, math.floor(camera.y / BLOCK_SIZE) - 1)
    end_y = min(
        world.WORLD_HEIGHT,
        math.floor((camera.y + HEIGHT) / BLOCK_SIZE) + 2,
    )

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            name = world.get_block(x, y)
            if name is None:
                continue

            screen_x = x * BLOCK_SIZE - camera.x
            screen_y = y * BLOCK_SIZE - camera.y
            screen.blit(TEXTURES[name], (round(screen_x), round(screen_y)))

    # Рисуем игрока в экранных координатах, не меняя его мировую позицию.
    old_x, old_y = player.x, player.y
    player.x -= camera.x
    player.y -= camera.y
    player.draw(screen)
    player.x, player.y = old_x, old_y

    pygame.display.flip()

pygame.quit()
