from collections import deque
from enum import Enum, unique
from pathlib import Path

Coord = tuple[int, int]


@unique
class Directions(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def step(self, pos: Coord) -> Coord:
        x, y = pos
        dx, dy = self.value
        return (x + dx, y + dy)

    def n_step(self, pos: Coord, n: int) -> Coord:
        x, y = pos
        dx, dy = self.value
        return (x + n * dx, y + n * dy)


UP = Directions.UP
DOWN = Directions.DOWN
LEFT = Directions.LEFT
RIGHT = Directions.RIGHT


def parse_input_part_1(filename: str) -> list[tuple[Directions, int]]:
    lines = Path(filename).read_text().splitlines()

    direction_lookup = {
        "U": Directions.UP,
        "D": Directions.DOWN,
        "L": Directions.LEFT,
        "R": Directions.RIGHT,
    }

    return [
        (direction_lookup[(parts := line.split())[0]], int(parts[1])) for line in lines
    ]


def parse_input_part_2(filename: str) -> list[tuple[Directions, int]]:
    lines = Path(filename).read_text().splitlines()

    direction_lookup = {
        "0": Directions.RIGHT,
        "1": Directions.DOWN,
        "2": Directions.LEFT,
        "3": Directions.UP,
    }

    result = []

    for line in lines:
        color_part = line.split()[2][2:-1]
        direction = direction_lookup[color_part[5]]
        count = int(color_part[0:5], base=16)
        result.append((direction, count))

    return result


def measure_trench(trench_instructions: list[tuple[Directions, int]]) -> int:
    start = (0, 0)
    trench = {start: "#"}

    current = start
    for dir, count in trench_instructions:
        for _ in range(count):
            current = dir.step(current)
            trench[current] = "#"

    # replace corners with other characters
    keys = list(trench.keys())
    for pos in keys:
        if UP.step(pos) in trench and RIGHT.step(pos) in trench:
            trench[pos] = "L"
        if UP.step(pos) in trench and LEFT.step(pos) in trench:
            trench[pos] = "J"
        if DOWN.step(pos) in trench and RIGHT.step(pos) in trench:
            trench[pos] = "F"
        if DOWN.step(pos) in trench and LEFT.step(pos) in trench:
            trench[pos] = "7"

    x_coords = [x for x, _ in trench]
    y_coords = [y for _, y in trench]

    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    result = 0

    # print the outline
    # for y in range(min_y, max_y + 1):
    #     for x in range(min_x, max_x + 1):
    #         current = (x, y)
    #         if current in trench:
    #             print(trench[current], end='')
    #         else:
    #             print(".", end='')
    #     print()

    # print()
    # print()

    for y in range(min_y, max_y + 1):
        inside = False
        corner = None

        for x in range(min_x, max_x + 1):
            current = (x, y)
            if current in trench:
                char = trench[current]
                if char in "FL":
                    corner = char
                elif char == "#":
                    if not corner:
                        inside = not inside
                elif char in "J7":
                    if (corner == "F" and char == "J") or (
                        corner == "L" and char == "7"
                    ):
                        inside = not inside
                    corner = None
                result += 1
                # print("#", end='')
            else:
                if inside:
                    result += 1
                    # print("#", end='')
                # else:
                # print(".", end='')
        # print()

    return result


def measure_trench_with_shoelace_formula(
    trench_instructions: list[tuple[Directions, int]]
) -> int:
    start = (0, 0)
    coordinates = [start]



    current = start
    for dir, count in trench_instructions:
        current = dir.n_step(current, count)
        coordinates.append(current)

    area = 0

    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]

        area += (y1 + y2) * (x1 - x2)

    area = abs(area)

    for _, count in trench_instructions:
        area += count

    area += 2 # why????

    return area // 2


def part_1():
    puzzle_input = parse_input_part_1("input.txt")
    # return measure_trench(puzzle_input)
    return measure_trench_with_shoelace_formula(puzzle_input)


def part_2():
    puzzle_input = parse_input_part_2("input.txt")
    return measure_trench_with_shoelace_formula(puzzle_input)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
