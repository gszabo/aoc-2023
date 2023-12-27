from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

Coord = tuple[int, int, int]


@dataclass
class Brick:
    x1: int
    y1: int
    z1: int

    x2: int
    y2: int
    z2: int

    def direction(self) -> str:
        if self.x1 != self.x2:
            return "x"

        if self.y1 != self.y2:
            return "y"

        return "z"

    def is_vertical(self) -> bool:
        return self.direction() == "z"

    def is_on_ground(self) -> bool:
        return self.z1 == 1 or self.z2 == 1

    def size(self) -> int:
        dir = self.direction()

        prop1 = getattr(self, dir + "1")
        prop2 = getattr(self, dir + "2")

        return prop2 - prop1 + 1

    def contains(self, x: int, y: int, z: int) -> bool:
        return (
            self.x1 <= x <= self.x2
            and self.y1 <= y <= self.y2
            and self.z1 <= z <= self.z2
        )

    def coords(self) -> list[Coord]:
        return [
            (x, y, self.z1)
            for x in range(self.x1, self.x2 + 1)
            for y in range(self.y1, self.y2 + 1)
        ]

    def coords_below(self) -> list[Coord]:
        return [
            (x, y, self.z1 - 1)
            for x in range(self.x1, self.x2 + 1)
            for y in range(self.y1, self.y2 + 1)
        ]

    def coords_above(self) -> list[Coord]:
        return [
            (x, y, self.z2 + 1)
            for x in range(self.x1, self.x2 + 1)
            for y in range(self.y1, self.y2 + 1)
        ]

    def move_down(self):
        self.z1 -= 1
        self.z2 -= 1


def parse_input(filename: str) -> list[Brick]:
    lines = Path(filename).read_text().splitlines()

    bricks = []

    for line in lines:
        coords1, coords2 = line.split("~")
        x1, y1, z1 = map(int, coords1.split(","))
        x2, y2, z2 = map(int, coords2.split(","))

        bricks.append(Brick(x1, y1, z1, x2, y2, z2))

    return bricks


def to_char(i: int) -> str:
    return chr(ord("A") + i)


def part_1():
    bricks = parse_input("input.txt")

    space = defaultdict(lambda: -1)

    for index, brick in enumerate(bricks):
        for coord in brick.coords():
            space[coord] = index

    # pprint(bricks)

    # let everything fall down and settle
    # print("Starting to move bricks down...")
    while True:
        move_happened = False

        for index, brick in enumerate(bricks):
            if brick.is_on_ground():
                # print("Brick", index, "is on ground")
                continue

            while not brick.is_on_ground() and all(
                space[coord] == -1 for coord in brick.coords_below()
            ):
                for coord in brick.coords():
                    space[coord] = -1

                # print("Moving brick", index, "down")
                brick.move_down()
                # print("New coords:", brick)
                for coord in brick.coords():
                    space[coord] = index

                move_happened = True

        if not move_happened:
            break

    # print("Falling finished")

    # find out which brick supports which bricks
    supports = defaultdict(set)
    supported_by = defaultdict(set)

    # pprint(bricks)

    for index, brick in enumerate(bricks):
        if brick.is_on_ground():
            # todo: do I need this?
            supported_by[index].add("ground")
            continue

        for coord in brick.coords_below():
            brick_index_below = space[coord]
            if brick_index_below != -1:
                supports[brick_index_below].add(index)
                supported_by[index].add(brick_index_below)

    removable = []

    for index in range(len(bricks)):
        is_index_removable = True

        for supported_index in supports[index]:
            if len(supported_by[supported_index]) == 1:
                # only `index` supports `supported_index`, so we cannot disintegrate `index`
                is_index_removable = False

        if is_index_removable:
            removable.append(index)

    # print("Removable:", [to_char(x) for x in removable])
    return len(set(removable))


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
