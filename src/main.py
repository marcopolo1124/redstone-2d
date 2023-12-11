# Importing the library
import pygame
from Block import world_map, Block
from Redstone import RedstoneTorch, RedstoneSource, RedstoneRepeater, redstone_placement
from Mechanism import Mechanism
from config import world_size
from AllBlocks import placeable_list, images

clock = pygame.time.Clock()
block_size = 50
WIDTH = world_size[0] * block_size
HEIGHT = world_size[1] * block_size

# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((WIDTH, HEIGHT))

# Initializing Color
BLACK = (0, 0, 0)

loaded_images = {}
for image in images:
    loaded_image = pygame.image.load(f"images/{image}")
    scaled_image = pygame.transform.scale(loaded_image, (block_size, block_size))
    loaded_images[image] = scaled_image


def draw_map():
    for x, row in enumerate(world_map):
        for y in range(len(row)):
            blk = Block.get_block(x, y)
            x_pos = x * block_size
            y_pos = y * block_size
            if blk:
                img, orientation = blk.image(x, y)
                rotated_image = pygame.transform.rotate(
                    loaded_images[img], -90 * orientation
                )
                surface.blit(rotated_image, (y_pos, x_pos))
            else:
                rect = pygame.Rect(y_pos, x_pos, block_size, block_size)
                pygame.draw.rect(surface, BLACK, rect, 1)


run = True
current_block_idx = 0
orientation = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_block_idx = 0
            if event.key == pygame.K_2:
                current_block_idx = 1
            if event.key == pygame.K_3:
                current_block_idx = 2
            if event.key == pygame.K_4:
                current_block_idx = 3
            if event.key == pygame.K_5:
                current_block_idx = 4
            if event.key == pygame.K_6:
                current_block_idx = 5
            if event.key == pygame.K_7:
                current_block_idx = 6
            if event.key == pygame.K_UP:
                orientation = 0
            if event.key == pygame.K_RIGHT:
                orientation = 1
            if event.key == pygame.K_DOWN:
                orientation = 2
            if event.key == pygame.K_LEFT:
                orientation = 3
        if event.type == pygame.MOUSEBUTTONDOWN:
            y, x = pygame.mouse.get_pos()
            idy = y // block_size
            idx = x // block_size
            if event.button == 1:
                Block.break_block(idx, idy)
            if event.button == 3:
                placed = placeable_list[current_block_idx].place(idx, idy, orientation)
                if not placed:
                    current_block = Block.get_block(idx, idy)
                    current_block.interact(idx, idy)

    state_changed = False
    state_changed = state_changed or RedstoneTorch.listen()
    state_changed = state_changed or RedstoneRepeater.listen()
    if state_changed:
        RedstoneSource.traverse_all()
    Mechanism.listen()

    surface.fill((255, 255, 255))
    draw_map()
    pygame.display.flip()
    clock.tick(5)

pygame.quit()
