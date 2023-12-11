from Mechanism import Mechanism
from Redstone import RedstoneTorch, redstone_placement
from Block import world_map, Block
from config import (
    world_size,
)
from all_blocks import (
    redstone_dust,
    redstone_torch,
    dirt_block,
    sticky_piston,
    obsidian,
)

redstone_torch.place(1, 1, 0)
redstone_torch.place(0, 15, 3)
sticky_piston.place(0, 0, 1)
dirt_block.place(0, 1, 1)
print("placed", obsidian.place(0, 4, 0))
for x, row in enumerate(world_map):
    for y in range(len(row)):
        redstone_dust.place(x, y, 0)

Block.break_block(0, 5)


def debug_redstone():
    debug_map = [[0] * world_size[0] for _ in range(world_size[1])]
    for x, row in enumerate(world_map):
        for y in range(len(row)):
            if (x, y) in redstone_placement:
                debug_map[x][y] = redstone_placement[(x, y)]["power"]
    for row in debug_map:
        print(row)


def debug_world():
    debug_map = [["."] * world_size[0] for _ in range(world_size[1])]
    for x, row in enumerate(debug_map):
        for y in range(len(row)):
            blk = Block.get_block(x, y)
            if blk is not None:
                debug_map[x][y] = blk.name
    for row in debug_map:
        print(row)


print("redstone")
debug_redstone()
print("world")
debug_world()
Mechanism.listen()
RedstoneTorch.listen()

print("redstone")
debug_redstone()
print("world")
debug_world()

Block.break_block(0, 4)
Mechanism.listen()
RedstoneTorch.listen()
print("redstone")
debug_redstone()
print("world")
debug_world()

Block.break_block(1, 0)
Mechanism.listen()
RedstoneTorch.listen()
print("redstone")
debug_redstone()
print("world")
debug_world()
