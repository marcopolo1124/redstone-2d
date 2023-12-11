from Redstone import Redstone, redstone_placement
from Block import Block, Placeable, world_map


class MechanicalBlock(Block):
    def destroy(self, x, y):
        super().destroy(x, y)
        Mechanism.break_block(x, y)

    def move(self, initial, dest):
        if not self.pushable:
            return
        init_x, init_y = initial
        mechanism: Mechanism = world_map[init_x][init_y]["mechanism"]
        orientation = world_map[init_x][init_y]["orientation"]
        Block.break_block(*initial)
        mechanism.place(*dest, orientation)


class Mechanism(Placeable):
    mechanisms = {}

    def __init__(self, redstone):
        self.redstone: Redstone = redstone

    def place(self, x, y, orientation):
        self.mechanisms[(x, y)] = {"mechanism": self, "on": False}
        self.redstone.place(x, y, orientation)

    @classmethod
    def break_block(self, x, y):
        if (x, y) not in self.mechanisms:
            return
        redstone: Redstone = self.mechanisms[(x, y)]["mechanism"].redstone
        redstone.destroy(x, y)
        del self.mechanisms[(x, y)]

    def execute(self, x, y) -> bool:
        print(f"executing at {x}, {y}")
        return True

    def stop(self, x, y) -> bool:
        print(f"stopping at {x}, {y}")
        return True

    @classmethod
    def listen(self):
        mechanisms = self.mechanisms.copy()
        for coord, mechanism in mechanisms.items():
            if coord in self.mechanisms:
                power = redstone_placement[coord]["power"]
                if power > 0 and not mechanism["on"]:
                    if mechanism["mechanism"].execute(*coord):
                        mechanism["on"] = True
                if power <= 0 and mechanism["on"]:
                    if mechanism["mechanism"].stop(*coord):
                        mechanism["on"] = False


class AbstractPiston(Mechanism):
    def __init__(self, piston, piston_extended, piston_head):
        super().__init__(Redstone([1, 2, 3], [], 0))
        self.piston: Block = piston
        self.piston_extended: Block = piston_extended
        self.piston_head: Block = piston_head

    def place(self, x, y, orientation):
        placed = self.piston.place(x, y, orientation)
        if placed:
            super().place(x, y, orientation)
            world_map[x][y]["mechanism"] = self
            print(world_map[x][y])

    @classmethod
    def break_block(self, x, y):
        Block.break_block(x, y)
        super().break_block(x, y)

    def execute(self, x, y):
        orientation = Block.get_block_orientation(x, y)
        x_dir, y_dir = Block.get_block_direction(x, y)
        curr_x, curr_y = x + x_dir, y + y_dir
        current_block = Block.get_block(curr_x, curr_y)
        push_count = 0
        while (
            push_count < 20
            and Block.is_inbound(curr_x, curr_y)
            and current_block is not None
            and current_block.pushable
        ):
            curr_x += x_dir
            curr_y += y_dir
            push_count += 1
            current_block = Block.get_block(curr_x, curr_y)

        if current_block is None:
            curr_x -= x_dir
            curr_y -= y_dir

        for _ in range(push_count):
            current_block = Block.get_block(curr_x, curr_y)
            current_block.move((curr_x, curr_y), (curr_x + x_dir, curr_y + y_dir))
            curr_x -= x_dir
            curr_y -= y_dir

        if self.piston_head.place(x + x_dir, y + y_dir, orientation):
            Block.replace(x, y, self.piston_extended)
            return True
        return False

    def stop(self, x, y):
        x_dir, y_dir = Block.get_block_direction(x, y)
        if Block.get_block(x, y) is self.piston_extended:
            Block.replace(x, y, self.piston)

        ph_x, ph_y = x + x_dir, y + y_dir
        if Block.get_block(ph_x, ph_y) is self.piston_head:
            Block.break_block(ph_x, ph_y)
        return True


class AbstractStickyPiston(AbstractPiston):
    def stop(self, x, y):
        x_dir, y_dir = Block.get_block_direction(x, y)
        if Block.get_block(x, y) is self.piston_extended:
            Block.replace(x, y, self.piston)

        ph_x, ph_y = x + x_dir, y + y_dir
        if Block.get_block(ph_x, ph_y) is self.piston_head:
            Block.break_block(ph_x, ph_y)

        adj_x, adj_y = ph_x + x_dir, ph_y + y_dir
        adjacent_block = Block.get_block(adj_x, adj_y)
        if adjacent_block:
            adjacent_block.move((adj_x, adj_y), (ph_x, ph_y))

        return True
