import pygame
from block_registry import BlockRegistry
from player import Player

pygame.init()
WIDTH, HEIGHT = 1280, 720
FPS = 60
BLOCK_SIZE = 64
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

registry = BlockRegistry()
registry.load()
stone = registry.get('stone')
texture = pygame.transform.scale(pygame.image.load(f'assets/blocks/{stone.texture}').convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE))

player = Player(400, 200)
platform = [{'x': x * BLOCK_SIZE, 'y': 0} for x in range(15)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()

    keys = pygame.key.get_pressed()
    mouse_x, _ = pygame.mouse.get_pos()
    player.update(keys, mouse_x)

    screen.fill((135,206,235))

    for block in platform:
        screen.blit(texture, (block['x'], HEIGHT // 2 + block['y']))

    player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()