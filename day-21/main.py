from pathlib import Path


Coord = tuple[int, int]


def parse_input(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()

    width = len(lines[0])
    height = len(lines)

    field = {}

    for y in range(height):
        for x in range(width):
            cell = lines[y][x]
            if cell == "S":
                start = (x, y)
            field[(x, y)] = cell if cell != "S" else "."


    return {"field": field, "width": width, "height": height, "start": start}


def part_1():
    data = parse_input("input.txt")
    step_count = 64

    field = data["field"]
    start = data["start"]

    reachable = {start}

    for _ in range(step_count):
        new_reachable = set()

        for x, y in reachable:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                new_x = x + dx
                new_y = y + dy
                if field.get((new_x, new_y)) == ".":
                    new_reachable.add((new_x, new_y))

        reachable = new_reachable

    return len(reachable)



def part_2():
    data = parse_input("input_sample.txt")
    step_count = 500

    field = data["field"]
    start = data["start"]
    width = data["width"]
    height = data["height"]

    reachable = {start}

    for _ in range(step_count):
        new_reachable = set()

        for x, y in reachable:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                new_x = x + dx
                new_y = y + dy
                if field[(new_x % width, new_y % height)] == ".":
                    new_reachable.add((new_x, new_y))

        reachable = new_reachable

    return len(reachable)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
