from config import world_size

world_map = [[None] * world_size[0] for _ in range(world_size[1])]
ORIENTATIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Placeable:
    def place(self, x, y, orientation):
        raise NotImplementedError

    @classmethod
    def break_block(self, x, y):
        raise NotImplementedError

    @classmethod
    def interact(self, x, y):
        return


class Block(Placeable):
    def __init__(self, name: str, pushable: bool = True, image_name=""):
        self.name = name
        self.pushable = pushable
        self.image_name = image_name

    def image(self, x, y):
        if len(self.image_name) > 0:
            return self.image_name, Block.get_block_orientation(x, y)
        return None

    def __repr__(self):
        return f"Block({self.name}, {self.pushable})"

    @staticmethod
    def is_inbound(x, y):
        if 0 <= x < world_size[1] and 0 <= y < world_size[0]:
            return True
        return False

    @classmethod
    def get_block_direction(self, x, y):
        if not self.is_inbound(x, y):
            raise IndexError()
        if world_map[x][y] is None:
            return (0, 0)
        else:
            return ORIENTATIONS[world_map[x][y]["orientation"]]

    @classmethod
    def get_block_orientation(self, x, y):
        if not self.is_inbound(x, y):
            raise IndexError()
        if world_map[x][y] is None:
            return 0
        else:
            return world_map[x][y]["orientation"]

    @classmethod
    def get_block(self, x, y):
        if not self.is_inbound(x, y) or world_map[x][y] is None:
            return None
        else:
            blk: Block = world_map[x][y]["block"]
            return blk

    @classmethod
    def get(self, x, y):
        if not self.is_inbound(x, y):
            raise IndexError()
        if world_map[x][y] is None:
            return None
        else:
            return {
                "block": world_map[x][y]["block"],
                "orientation": self.orientations[world_map[x][y]["orientation"]],
            }

    def place(self, x: int, y: int, orientation: int):
        if self.is_inbound(x, y) and world_map[x][y] is None:
            world_map[x][y] = {"block": self, "orientation": orientation % 4}
            return True
        return False

    @classmethod
    def destroy(cls, x: int, y: int):
        """interface function that completely removes all traces of the block"""
        if cls.is_inbound(x, y):
            world_map[x][y] = None

    @classmethod
    def replace(cls, x: int, y: int, new_block):
        """
        interface function that removes the block from the world map ONLY
        redstone and mechanism maps are still intact
        """
        if cls.is_inbound(x, y):
            world_map[x][y]["block"] = new_block

    @classmethod
    def break_block(cls, x: int, y: int):
        blk = Block.get_block(x, y)
        if blk is not None:
            blk.destroy(x, y)

    def move(self, initial: (int, int), dest: (int, int)):
        if not self.pushable:
            return False

        init_x, init_y = initial
        dest_x, dest_y = dest
        if (
            self.is_inbound(init_x, init_y)
            and self.is_inbound(dest_x, dest_y)
            and world_map[dest_x][dest_y] is None
        ):
            blk = self.get_block(init_x, init_y)
            orientation = self.get_block_orientation(init_x, init_y)
            Block.break_block(init_x, init_y)
            blk.place(dest_x, dest_y, orientation)
            return True
        return False
