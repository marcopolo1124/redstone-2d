from Block import Block, ORIENTATIONS
from collections import deque

redstone_placement = {}


class Redstone:
    traversed = set()

    def __init__(self, input_ports: list[int], output_ports: list[int], power: int = 0):
        # ports are numbered 0 - 3, 0 -> up, 1 -> right, 2, down, 3, left
        self.output_ports = output_ports
        self.input_ports = input_ports
        self.power = power

    def __repr__(self):
        return f"Redstone({self.output_ports}, {self.input_ports})"

    def get_power(self, x, y):
        max_power = 0
        prev_blocks = self.get_prev_blocks(x, y)
        for rs_blk in prev_blocks.values():
            if rs_blk["power"] - 1 > max_power:
                max_power = rs_blk["power"] - 1
        return max(self.power, max_power)

    def place(self, x, y, orientation):
        if (x, y) in redstone_placement:
            return

        power = self.power

        redstone_placement[(x, y)] = {
            "redstone": self,
            "power": self.power,
            "orientation": orientation,
        }

        power = self.get_power(x, y)
        if power > 0:
            self.traversed.add((x, y))

        redstone_placement[(x, y)]["power"] = power
        Redstone.traverse(x, y, power)

    def set_power(self, x, y, power):
        if (x, y) in redstone_placement:
            redstone_placement[(x, y)]["power"] = power
            return power
        return 0

    @classmethod
    def traverse(cls, x, y, power):
        bfs_queue = deque()
        bfs_queue.append((x, y, power))

        while bfs_queue:
            curr_x, curr_y, curr_power = bfs_queue.popleft()
            next_blocks = Redstone.get_next_blocks(curr_x, curr_y)
            for blk, state in next_blocks.items():
                if state["power"] < curr_power - 1 or blk not in cls.traversed:
                    new_power = state["redstone"].set_power(*blk, curr_power - 1)
                    bfs_queue.appendleft((*blk, new_power))
                    cls.traversed.add(blk)

    @classmethod
    def destroy(self, x, y):
        if (x, y) in redstone_placement:
            del redstone_placement[(x, y)]

    @staticmethod
    def output_port_orientation(x, y):
        """
        Get the coordinates each output port is connected to at
        redstone component x, y given the block's orientation
        """
        if (x, y) not in redstone_placement:
            return
        redstone_state = redstone_placement[(x, y)]
        output_ports = redstone_state["redstone"].output_ports
        orientation = redstone_state["orientation"]

        oriented_output_ports = []
        for output_port in output_ports:
            x_dir, y_dir = ORIENTATIONS[(output_port + orientation) % 4]
            if (x + x_dir, y + y_dir) in redstone_placement:
                oriented_output_ports.append((x + x_dir, y + y_dir))
        return oriented_output_ports

    @staticmethod
    def input_port_orientation(x, y):
        """
        Get the coordinates each input port is connected to at
        redstone component x, y given the block's orientation
        """
        if (x, y) not in redstone_placement:
            return []
        redstone_state = redstone_placement[(x, y)]
        input_ports = redstone_state["redstone"].input_ports
        orientation = redstone_state["orientation"]

        oriented_input_ports = []
        for input_port in input_ports:
            x_dir, y_dir = ORIENTATIONS[(input_port + orientation) % 4]
            if (x + x_dir, y + y_dir) in redstone_placement:
                oriented_input_ports.append((x + x_dir, y + y_dir))
        return oriented_input_ports

    @staticmethod
    def get_next_blocks(x, y):
        output_ports: list[tuple[int, int]] = Redstone.output_port_orientation(x, y)
        res = {}
        for out in output_ports:
            input_ports = Redstone.input_port_orientation(*out)
            if (x, y) in input_ports:
                res[out] = redstone_placement[out]
        return res

    @staticmethod
    def get_prev_blocks(x, y):
        input_ports: list[tuple[int, int]] = Redstone.input_port_orientation(x, y)
        res = {}
        for input in input_ports:
            output_ports = Redstone.output_port_orientation(*input)
            if (x, y) in output_ports:
                res[input] = redstone_placement[input]
        return res


class RedstoneSource(Redstone):
    redstone_sources = {}

    def set_power(self, x, y, power):
        if (x, y) not in self.redstone_sources:
            return 0
        if self.redstone_sources[(x, y)]:
            super().set_power(x, y, self.power)
            return self.power
        else:
            super().set_power(x, y, 0)
            return 0

    def __init__(self, input_ports, output_ports, power):
        super().__init__(input_ports, output_ports, power)

    def place(self, x, y, orientation):
        super().place(x, y, orientation)
        self.redstone_sources[(x, y)] = True

    def destroy(self, x, y):
        super().destroy(x, y)
        del self.redstone_sources[(x, y)]

    @classmethod
    def traverse_all(self):
        self.traversed.clear()

        for source, active in self.redstone_sources.items():
            if active:
                power = redstone_placement[source]["redstone"].power
                redstone_placement[source]["power"] = power
                self.traverse(*source, power)
        for redstone in redstone_placement:
            if redstone not in self.traversed:
                redstone_placement[redstone]["redstone"].set_power(*redstone, 0)

    @classmethod
    def detect_state_change(self, x, y):
        current_state = self.redstone_sources[(x, y)]
        prev_blocks = Redstone.get_prev_blocks(x, y)
        new_state = True
        state_changed = False
        for state in prev_blocks.values():
            power = state["power"]
            if power > 1:
                new_state = False
            else:
                new_state = True
            state_changed = state_changed or current_state != new_state

        state_changed = state_changed or current_state != new_state

        return state_changed, new_state


class RedstoneTorch(RedstoneSource):
    torches = set()

    def place(self, x, y, orientation):
        super().place(x, y, orientation)
        self.torches.add((x, y))

    def get_power(self, x, y):
        max_power = 0
        prev_blocks = self.get_prev_blocks(x, y)
        for rs_blk in prev_blocks.values():
            if rs_blk["power"] - 1 > max_power:
                max_power = rs_blk["power"] - 1
        if max_power > 0:
            return 0
        return self.power

    def destroy(self, x, y):
        super().destroy(x, y)
        self.torches.remove((x, y))

    @classmethod
    def listen(self):
        state_changed = False
        for torch in self.torches:
            curr_state_changed, new_state = self.detect_state_change(*torch)
            self.redstone_sources[torch] = new_state
            state_changed = state_changed or curr_state_changed

        return state_changed


class RedstoneBlock(Block):
    def __init__(self, name, pushable, redstone: Redstone, on_image="", off_image=""):
        super().__init__(name, pushable)
        self.redstone = redstone
        self.on_image = on_image
        self.off_image = off_image

    def image(self, x, y):
        if (x, y) not in redstone_placement:
            return None
        orientation = Block.get_block_orientation(x, y)
        if redstone_placement[(x, y)]["power"] > 0:
            return self.on_image, orientation
        return self.off_image, orientation

    def __repr__(self):
        return f"RedstoneBlock({self.name, self.pushable, self.redstone})"

    def place(self, x, y, orientation):
        placed = super().place(x, y, orientation)
        if placed:
            self.redstone.place(x, y, orientation)
            return True
        return False

    def destroy(self, x, y):
        super().destroy(x, y)
        self.redstone.destroy(x, y)
        RedstoneSource.traverse_all()


class RedstoneRepeater(RedstoneSource):
    repeaters = {}
    max_tick = 4
    on_power = 16

    def __init__(self, input_ports, output_ports):
        super().__init__(input_ports, output_ports, 16)

    def set_power(self, x, y, power):
        if power > 0:
            self.reset_on_delay(x, y)
        else:
            self.reset_off_delay(x, y)
        return redstone_placement[(x, y)]["power"]

    def place(self, x, y, orientation):
        if (x, y) in redstone_placement:
            return
        redstone_placement[(x, y)] = {
            "redstone": self,
            "power": 0,
            "orientation": orientation,
        }
        prev_blocks = self.get_prev_blocks(x, y)
        power = 0
        for rs_blk in prev_blocks.values():
            if rs_blk["power"] - 1 > power:
                power = rs_blk["power"] - 1
                self.traversed.add((x, y))

        self.repeaters[(x, y)] = {"delay": 0, "on_delay": -1, "off_delay": -1}
        redstone_placement[(x, y)]["redstone"].set_power(x, y, power)
        self.redstone_sources[(x, y)] = False

        Redstone.traverse(x, y, power)

    def set_delay(self, x, y, tick):
        tick %= self.max_tick
        print(tick)
        self.repeaters[(x, y)]["delay"] = tick

    def update_delay(self, x, y):
        delay = self.repeaters[(x, y)]["delay"]
        self.set_delay(x, y, delay + 1)

    @classmethod
    def reset_on_delay(self, x, y):
        if (
            self.repeaters[(x, y)]["on_delay"] < 0
            and redstone_placement[(x, y)]["power"] <= 0
        ):
            delay = self.repeaters[(x, y)]["delay"]
            self.repeaters[(x, y)]["on_delay"] = delay

    @classmethod
    def reset_off_delay(self, x, y):
        if (
            self.repeaters[(x, y)]["off_delay"] < 0
            and redstone_placement[(x, y)]["power"] > 0
        ):
            self.repeaters[(x, y)]["off_delay"] = self.repeaters[(x, y)]["delay"]

    def destroy(self, x, y):
        super().destroy(x, y)
        del self.repeaters[(x, y)]

    @classmethod
    def listen(self):
        changed_state = False
        for repeater, state in self.repeaters.items():
            if state["on_delay"] == 0:
                redstone_placement[repeater]["power"] = self.on_power
                state["on"] = True
                self.redstone_sources[repeater] = True
                Redstone.traverse(*repeater, self.on_power)
                state["on_delay"] -= 1

            elif state["off_delay"] == 0:
                self.redstone_sources[repeater] = False
                redstone_placement[repeater]["power"] = 0
                state["on"] = False
                changed_state = True
                state["off_delay"] -= 1

            if state["on_delay"] > 0 and state["off_delay"] > 0:
                if state["on_delay"] > state["off_delay"]:
                    state["off_delay"] -= 1
                else:
                    state["on_delay"] -= 1

            elif state["on_delay"] > 0:
                state["on_delay"] -= 1
            elif state["off_delay"] > 0:
                state["off_delay"] -= 1

        return changed_state


class RedstoneRepeaterBlock(RedstoneBlock):
    def __init__(self, name, pushable, redstone: RedstoneRepeater, on_image, off_image):
        super().__init__(name, pushable, redstone, on_image, off_image)
        self.redstone = redstone

    def __repr__(self):
        return f"RedstoneRepeaterBlock"

    def interact(self, x, y):
        self.redstone.update_delay(x, y)
