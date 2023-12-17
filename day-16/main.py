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


HORIZONTAL = {Directions.LEFT, Directions.RIGHT}
VERTICAL = {Directions.UP, Directions.DOWN}


def parse_input(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()
    width = len(lines[0])
    height = len(lines)
    return {
        "width": width,
        "height": height,
        "matrix": {(x, y): lines[y][x] for x in range(width) for y in range(height)},
    }


def next_coord(pos: Coord, dir: Directions) -> Coord:
    x, y = pos
    dx, dy = dir.value
    return (x + dx, y + dy)


def enter_light(
    start: tuple[Coord, Directions], matrix: dict[Coord, str]
) -> set[Coord]:
    visited = set()

    # to avoid endless reflection cycles and to be able to visit the same node with different direction
    visited_with_direction = set()

    queue = deque([start])
    while len(queue) > 0:
        current_pos, dir = queue.popleft()
        visited.add(current_pos)
        visited_with_direction.add((current_pos, dir))

        ch = matrix[current_pos]

        if ch == ".":
            next_pos = next_coord(current_pos, dir)
            if next_pos in matrix and (next_pos, dir) not in visited_with_direction:
                queue.appendleft((next_pos, dir))
        elif ch == "/":
            if dir == Directions.UP:
                next_dir = Directions.RIGHT
            elif dir == Directions.DOWN:
                next_dir = Directions.LEFT
            elif dir == Directions.LEFT:
                next_dir = Directions.DOWN
            elif dir == Directions.RIGHT:
                next_dir = Directions.UP

            next_pos = next_coord(current_pos, next_dir)
            if (
                next_pos in matrix
                and (next_pos, next_dir) not in visited_with_direction
            ):
                queue.appendleft((next_pos, next_dir))
        elif ch == "\\":
            if dir == Directions.UP:
                next_dir = Directions.LEFT
            elif dir == Directions.DOWN:
                next_dir = Directions.RIGHT
            elif dir == Directions.LEFT:
                next_dir = Directions.UP
            elif dir == Directions.RIGHT:
                next_dir = Directions.DOWN

            next_pos = next_coord(current_pos, next_dir)
            if (
                next_pos in matrix
                and (next_pos, next_dir) not in visited_with_direction
            ):
                queue.appendleft((next_pos, next_dir))
        elif ch == "|":
            if dir in VERTICAL:
                next_pos = next_coord(current_pos, dir)
                if next_pos in matrix and (next_pos, dir) not in visited_with_direction:
                    queue.appendleft((next_pos, dir))
            else:
                next_directions = [Directions.UP, Directions.DOWN]
                for next_dir in next_directions:
                    next_pos = next_coord(current_pos, next_dir)
                    if (
                        next_pos in matrix
                        and (next_pos, next_dir) not in visited_with_direction
                    ):
                        queue.appendleft((next_pos, next_dir))
        elif ch == "-":
            if dir in HORIZONTAL:
                next_pos = next_coord(current_pos, dir)
                if next_pos in matrix and (next_pos, dir) not in visited_with_direction:
                    queue.appendleft((next_pos, dir))
            else:
                next_directions = [Directions.LEFT, Directions.RIGHT]
                for next_dir in next_directions:
                    next_pos = next_coord(current_pos, next_dir)
                    if (
                        next_pos in matrix
                        and (next_pos, next_dir) not in visited_with_direction
                    ):
                        queue.appendleft((next_pos, next_dir))
        else:
            raise ValueError(f"Unexpected char {ch}")

    return visited


def part_1():
    puzzle_input = parse_input("input.txt")

    matrix = puzzle_input["matrix"]

    start = ((0, 0), Directions.RIGHT)

    visited = enter_light(start, matrix)

    return len(visited)


def part_2():
    puzzle_input = parse_input("input.txt")

    matrix = puzzle_input["matrix"]
    width = puzzle_input["width"]
    height = puzzle_input["height"]

    start_coords = []
    start_coords.extend(((x, 0), Directions.DOWN) for x in range(width))
    start_coords.extend(((x, height - 1), Directions.UP) for x in range(width))
    start_coords.extend(((0, y), Directions.RIGHT) for y in range(height))
    start_coords.extend(((width - 1, y), Directions.LEFT) for y in range(height))

    energized_cells = [
        len(enter_light(start, matrix)) for start in start_coords
    ]

    return max(energized_cells)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
