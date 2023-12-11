from Mechanism import AbstractPiston, AbstractStickyPiston, MechanicalBlock
from Block import Block, Placeable
from Redstone import (
    RedstoneBlock,
    Redstone,
    RedstoneTorch,
    RedstoneRepeater,
    RedstoneRepeaterBlock,
)

images = [
    "dirt.png",
    "obsidian.png",
    "piston_side.png",
    "piston_extension.png",
    "piston_extended_base.png",
    "redstone_torch.png",
    "redstone_torch_off.png",
    "redstone_dust_powered.png",
    "redstone_dust_unpowered.png",
    "redstone_repeater_on.png",
    "redstone_repeater_off.png",
]

piston_blk = MechanicalBlock("p", True, "piston_side.png")
piston_extended = MechanicalBlock("pe", False, "piston_extended_base.png")
piston_head = Block("ph", False, "piston_extension.png")
sticky_piston_blk = MechanicalBlock("sp", True, "piston_side.png")
sticky_piston_head = Block("sph", False, "piston_extension.png")


piston = AbstractPiston(piston_blk, piston_extended, piston_head)
sticky_piston = AbstractStickyPiston(
    sticky_piston_blk, piston_extended, sticky_piston_head
)

dirt_block = Block("D", True, "dirt.png")
obsidian = Block("O", False, "obsidian.png")
redstone_torch = RedstoneBlock(
    "rt",
    True,
    RedstoneTorch([2], [0, 1, 3], 16),
    "redstone_torch.png",
    "redstone_torch_off.png",
)
redstone_dust = RedstoneBlock(
    "rd",
    True,
    Redstone([0, 1, 2, 3], [0, 1, 2, 3]),
    "redstone_dust_powered.png",
    "redstone_dust_unpowered.png",
)

redstone_repeater = RedstoneRepeaterBlock(
    "rp",
    True,
    RedstoneRepeater([2], [0]),
    "redstone_repeater_on.png",
    "redstone_repeater_off.png",
)

placeable_list: list[Placeable] = [
    dirt_block,
    redstone_torch,
    redstone_dust,
    piston,
    sticky_piston,
    obsidian,
    redstone_repeater,
]
block_list: list[Block] = [
    dirt_block,
    redstone_torch,
    redstone_dust,
    piston_blk,
    sticky_piston_blk,
    piston_extended,
    piston_head,
    sticky_piston_head,
    obsidian,
    redstone_repeater,
]
