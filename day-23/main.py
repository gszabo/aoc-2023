from collections import deque
from pathlib import Path

Coord = tuple[int, int]


def parse_input(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()
    width = len(lines[0])
    height = len(lines)

    field = {}

    for y in range(height):
        for x in range(width):
            field[(x, y)] = lines[y][x]

    start = (lines[0].index("."), 0)
    end = (lines[-1].index("."), height - 1)

    return {
        "field": field,
        "start": start,
        "end": end,
        "width": width,
        "height": height,
    }


def print_field_with_path(
    field: dict[Coord, str], width: int, height: int, path: set[Coord]
):
    for y in range(height):
        for x in range(width):
            if (x, y) in path:
                print("O", end="")
            else:
                print(field[(x, y)], end="")
        print()


UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)


STEP_VECTORS = [UP, RIGHT, DOWN, LEFT]


def part_1():
    data = parse_input("input.txt")

    field = data["field"]
    start = data["start"]
    end = data["end"]

    def get_neighbors(coord: Coord, path: set[Coord]) -> list[Coord]:
        result = []

        for vector in STEP_VECTORS:
            possible = (coord[0] + vector[0], coord[1] + vector[1])

            if possible in path or possible not in field or field[possible] == "#":
                continue

            # print("Checking", possible, "with vector", vector, field[possible])

            if field[possible] == ".":
                result.append(possible)
            elif field[possible] == ">" and vector == RIGHT:
                result.append(possible)
            elif field[possible] == "v" and vector == DOWN:
                result.append(possible)

        return result

    def walk_until_possible(segment_start: Coord, path: set[Coord]):
        path = path.copy()

        current = segment_start
        while True:
            path.add(current)

            if current == end:
                return end, path

            neighbors = get_neighbors(current, path)

            if len(neighbors) != 1:
                return current, path

            current = neighbors[0]

    paths_till_end = []

    queue = deque([(start, {start})])
    while len(queue) > 0:
        current, path = queue.popleft()

        if current == end:
            paths_till_end.append(path)
            continue

        neighbors = get_neighbors(current, path)
        # print("Neighbors of", current, "are", neighbors)
        for neighbor in neighbors:
            segment_end, extended_path = walk_until_possible(neighbor, path | {neighbor})
            # print("Appending", segment_end, extended_path)
            queue.append((segment_end, extended_path))

    # print_field_with_path(data["field"], data["width"], data["height"], path)

    # The start field does not count into the path length, so we need to subtract 1
    return max(len(path) - 1 for path in paths_till_end)


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
