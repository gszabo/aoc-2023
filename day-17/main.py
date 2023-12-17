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

    def turn_left(self) -> "Directions":
        if self == Directions.UP:
            return Directions.LEFT
        if self == Directions.DOWN:
            return Directions.RIGHT
        if self == Directions.LEFT:
            return Directions.DOWN
        if self == Directions.RIGHT:
            return Directions.UP

    def turn_right(self) -> "Directions":
        if self == Directions.UP:
            return Directions.RIGHT
        if self == Directions.DOWN:
            return Directions.LEFT
        if self == Directions.LEFT:
            return Directions.UP
        if self == Directions.RIGHT:
            return Directions.DOWN

    def step(self, pos: Coord) -> Coord:
        x, y = pos
        dx, dy = self.value
        return (x + dx, y + dy)


def parse_input(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()
    width = len(lines[0])
    height = len(lines)
    return {
        "width": width,
        "height": height,
        "matrix": {
            (x, y): int(lines[y][x]) for x in range(width) for y in range(height)
        },
    }


def part_1():
    puzzle_input = parse_input("input.txt")

    matrix = puzzle_input["matrix"]
    width = puzzle_input["width"]
    height = puzzle_input["height"]

    # reversing the direction
    start = (width - 1, height - 1)
    end = (0, 0)

    result = {
        (start, Directions.UP, 0): matrix[start],
        (start, Directions.LEFT, 0): matrix[start],
    }

    queue = deque(list(result.keys()))
    while len(queue) > 0:
        item = queue.popleft()
        pos, dir, step_count = item

        directions = [dir.turn_left(), dir.turn_right()]
        if step_count < 3:
            directions.append(dir)

        for next_dir in directions:
            next_pos = next_dir.step(pos)
            next_step_count = step_count + 1 if next_dir == dir else 1
            if next_pos in matrix:
                key = (next_pos, next_dir, next_step_count)
                value_candidate = result[item] + matrix[next_pos]
                if key not in result or value_candidate < result[key]:
                    result[key] = value_candidate
                    queue.append(key)

    return min([result[key] for key in result if key[0] == end]) - matrix[end]


def part_2():
    puzzle_input = parse_input("input.txt")

    matrix = puzzle_input["matrix"]
    width = puzzle_input["width"]
    height = puzzle_input["height"]

    # reversing the direction
    start = (width - 1, height - 1)
    end = (0, 0)

    result = {
        (start, Directions.UP, 0): matrix[start],
        (start, Directions.LEFT, 0): matrix[start],
    }

    queue = deque(list(result.keys()))
    while len(queue) > 0:
        item = queue.popleft()
        pos, dir, step_count = item

        directions = []
        if step_count < 4:
            directions.append(dir)
        elif 4 <= step_count < 10:
            directions.append(dir)
            directions.append(dir.turn_left())
            directions.append(dir.turn_right())
        else:
            directions.append(dir.turn_left())
            directions.append(dir.turn_right())

        for next_dir in directions:
            next_pos = next_dir.step(pos)
            next_step_count = step_count + 1 if next_dir == dir else 1
            if next_pos in matrix:
                key = (next_pos, next_dir, next_step_count)
                value_candidate = result[item] + matrix[next_pos]
                if key not in result or value_candidate < result[key]:
                    result[key] = value_candidate
                    queue.append(key)

    return (
        min([result[key] for key in result if key[0] == end and key[2] >= 4])
        - matrix[end]
    )


if __name__ == "__main__":
    print("Part 1:", part_1())  # 18 sec
    print("Part 2:", part_2())  # 26 sec
