from collections import deque
from pathlib import Path


def get_neighbours(x: int, y: int, char: str) -> list[tuple[int, int]]:
    if char == "." or char == "S":
        return []
    if char == "-":
        return [(x + 1, y), (x - 1, y)]
    if char == "|":
        return [(x, y + 1), (x, y - 1)]
    if char == "L":
        return [(x, y - 1), (x + 1, y)]
    if char == "7":
        return [(x, y + 1), (x - 1, y)]
    if char == "J":
        return [(x, y - 1), (x - 1, y)]
    if char == "F":
        return [(x, y + 1), (x + 1, y)]

    raise ValueError(f"Unknown character: {char}")


def get_start_position(lines: list[str]) -> tuple[int, int]:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                return (x, y)
    raise ValueError("No start position found")


def are_neighbours(
    point_1: tuple[int, int],
    point_2: tuple[int, int],
    matrix: dict[tuple[int, int], list[tuple[int, int]]],
) -> bool:
    if point_1 not in matrix or point_2 not in matrix:
        return False

    for neigbour in matrix[point_1]:
        if neigbour == point_2:
            return True

    for neigbour in matrix[point_2]:
        if neigbour == point_1:
            return True

    return False


def parse_input(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()
    width = len(lines[0])
    height = len(lines)

    neighbour_matrix = {
        (x, y): get_neighbours(x, y, lines[y][x])
        for y in range(height)
        for x in range(width)
    }

    start_pos = get_start_position(lines)
    start_x, start_y = start_pos

    start_position_neighbour_candidates = [
        (start_x + 1, start_y),
        (start_x - 1, start_y),
        (start_x, start_y + 1),
        (start_x, start_y - 1),
    ]
    neigbours = [
        candidate
        for candidate in start_position_neighbour_candidates
        if are_neighbours(start_pos, candidate, neighbour_matrix)
    ]
    neighbour_matrix[start_pos] = neigbours

    return {
        "lines": [list(line) for line in lines],
        "matrix": neighbour_matrix,
        "width": width,
        "height": height,
        "start_pos": start_pos,
    }


def print_distances(distances: dict[tuple[int, int], int], width: int, height: int):
    for y in range(height):
        for x in range(width):
            d = distances[(x, y)]
            char_to_print = "." if d == -1 else str(d)
            print(char_to_print, end="")
        print()


def part_1():
    data = parse_input("input.txt")

    neighbour_matrix = data["matrix"]
    width = data["width"]
    height = data["height"]
    start_pos = data["start_pos"]

    distances = {(x, y): -1 for x in range(width) for y in range(height)}
    visited = {(x, y): False for x in range(width) for y in range(height)}

    distances[start_pos] = 0
    visited[start_pos] = True

    queue = deque([start_pos])
    while queue:
        current = queue.popleft()
        visited[current] = True

        for neighbour in neighbour_matrix[current]:
            if not visited[neighbour]:
                queue.append(neighbour)
                distances[neighbour] = distances[current] + 1

    return max(distances.values())


def sandbox():
    data = parse_input("input_sample.txt")

    neighbour_matrix = data["matrix"]
    width = data["width"]
    height = data["height"]
    start_pos = data["start_pos"]

    distances = {(x, y): -1 for x in range(width) for y in range(height)}
    visited = {(x, y): False for x in range(width) for y in range(height)}

    distances[start_pos] = 0
    visited[start_pos] = True

    queue = deque([start_pos])
    while queue:
        current = queue.popleft()
        visited[current] = True

        for neighbour in neighbour_matrix[current]:
            if not visited[neighbour]:
                queue.append(neighbour)
                distances[neighbour] = distances[current] + 1

    print_distances(distances, width, height)
    max_distance = max(distances.values())
    print(f"Max distance: {max_distance}")


def sandbox_2():
    data = parse_input("input.txt")
    # data = parse_input("input_sample_2.txt")

    lines = data["lines"]
    neighbour_matrix = data["matrix"]
    width = data["width"]
    height = data["height"]
    start_pos = data["start_pos"]

    main_loop = set()

    queue = deque([start_pos])
    while queue:
        current = queue.popleft()
        main_loop.add(current)

        for neighbour in neighbour_matrix[current]:
            if neighbour not in main_loop:
                queue.append(neighbour)

    # replace char of start_pos with corresponding char instead of "S"
    start_x, start_y = start_pos
    start_neighbours = set(neighbour_matrix[start_pos])
    if start_neighbours == {(start_x + 1, start_y), (start_x - 1, start_y)}:
        lines[start_y][start_x] = "-"
    elif start_neighbours == {(start_x, start_y + 1), (start_x, start_y - 1)}:
        lines[start_y][start_x] = "|"
    elif start_neighbours == {(start_x, start_y - 1), (start_x + 1, start_y)}:
        lines[start_y][start_x] = "L"
    elif start_neighbours == {(start_x, start_y + 1), (start_x - 1, start_y)}:
        lines[start_y][start_x] = "7"
    elif start_neighbours == {(start_x, start_y - 1), (start_x - 1, start_y)}:
        lines[start_y][start_x] = "J"
    elif start_neighbours == {(start_x, start_y + 1), (start_x + 1, start_y)}:
        lines[start_y][start_x] = "F"
    else:
        raise ValueError(
            f"Unknown neighbours: {start_neighbours}, start pos: {start_pos}"
        )

    # print("Replaced start char with:", lines[start_y][start_x])

    cleaned_lines = {
        (x, y): (lines[y][x] if (x, y) in main_loop else ".")
        for x in range(width)
        for y in range(height)
    }

    for y in range(height):
        for x in range(width):
            char_to_print = "."
            if (x, y) in main_loop:
                char_to_print = lines[y][x]
            print(char_to_print, end="")
        print()

    # find top left corner
    top_left_corner = None
    for y in range(height):
        for x in range(width):
            if cleaned_lines[(x, y)] == "F":
                top_left_corner = (x, y)
                break
        if top_left_corner:
            break

    if not top_left_corner:
        raise ValueError("No top left corner found")

    inside_cells_starting_points = set()

    # walk main loop counter clockwise from top left corner
    # cells to the left side of the main loop by this walking direction are inside cells
    current = top_left_corner
    direction = "left"
    while True:
        x, y = current

        current_char = cleaned_lines[current]

        next_direction = None

        lefts = []
        if current_char == "L":
            if direction == "down":
                lefts.append((x + 1, y - 1))
                next_direction = "right"
            elif direction == "left":
                lefts.append((x - 1, y + 1))
                lefts.append((x - 1, y))
                lefts.append((x, y - 1))
                next_direction = "up"
            else:
                raise ValueError(
                    f"Unknown direction: {direction} at {current} {current_char}"
                )
        elif current_char == "7":
            if direction == "up":
                lefts.append((x - 1, y + 1))
                next_direction = "left"
            elif direction == "right":
                lefts.append((x, y - 1))
                lefts.append((x + 1, y - 1))
                lefts.append((x + 1, y))
                next_direction = "down"
            else:
                raise ValueError(
                    f"Unknown direction: {direction} at {current} {current_char}"
                )
        elif current_char == "F":
            if direction == "left":
                lefts.append((x + 1, y + 1))
                next_direction = "down"
            elif direction == "up":
                lefts.append((x, y - 1))
                lefts.append((x - 1, y - 1))
                lefts.append((x - 1, y))
                next_direction = "right"
            else:
                raise ValueError(
                    f"Unknown direction: {direction} at {current} {current_char}"
                )
        elif current_char == "J":
            if direction == "right":
                lefts.append((x - 1, y - 1))
                next_direction = "up"
            elif direction == "down":
                lefts.append((x, y + 1))
                lefts.append((x + 1, y + 1))
                lefts.append((x + 1, y))
                next_direction = "left"
            else:
                raise ValueError(
                    f"Unknown direction: {direction} at {current} {current_char}"
                )
        elif current_char == "-":
            if direction == "left":
                lefts.append((x, y + 1))
            elif direction == "right":
                lefts.append((x, y - 1))
            else:
                raise ValueError(
                    f"Unknown direction: {direction} at {current} {current_char}"
                )
            next_direction = direction
        elif current_char == "|":
            if direction == "up":
                lefts.append((x - 1, y))
            elif direction == "down":
                lefts.append((x + 1, y))
            else:
                raise ValueError(
                    f"Unknown direction: {direction} at {current} {current_char}"
                )
            next_direction = direction

        for left in lefts:
            if cleaned_lines[left] == ".":
                inside_cells_starting_points.add(left)

        if next_direction == "down":
            next = (x, y + 1)
        if next_direction == "left":
            next = (x - 1, y)
        if next_direction == "up":
            next = (x, y - 1)
        if next_direction == "right":
            next = (x + 1, y)

        direction = next_direction
        current = next

        if current == top_left_corner:
            break

    print("inside_cells_starting_points", inside_cells_starting_points)
    inside_cells = set()
    queue = deque(inside_cells_starting_points)
    while queue:
        current = queue.popleft()
        x, y = current
        inside_cells.add(current)

        neighbours = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        for neighbour in neighbours:
            if neighbour not in inside_cells and cleaned_lines[neighbour] == ".":
                queue.append(neighbour)

    for y in range(height):
        for x in range(width):
            char_to_print = "."
            if (x, y) in main_loop:
                char_to_print = lines[y][x]
            elif (x, y) in inside_cells:
                char_to_print = "I"
            print(char_to_print, end="")
        print()

    print("len(inside_cells)", len(inside_cells))


def sandbox_reddit():
    # data = parse_input("input.txt")
    data = parse_input("input_sample_2.txt")

    lines = data["lines"]
    neighbour_matrix = data["matrix"]
    width = data["width"]
    height = data["height"]
    start_pos = data["start_pos"]

    main_loop = set()

    queue = deque([start_pos])
    while queue:
        current = queue.popleft()
        main_loop.add(current)

        for neighbour in neighbour_matrix[current]:
            if neighbour not in main_loop:
                queue.append(neighbour)

    # replace char of start_pos with corresponding char instead of "S"
    start_x, start_y = start_pos
    start_neighbours = set(neighbour_matrix[start_pos])
    if start_neighbours == {(start_x + 1, start_y), (start_x - 1, start_y)}:
        lines[start_y][start_x] = "-"
    elif start_neighbours == {(start_x, start_y + 1), (start_x, start_y - 1)}:
        lines[start_y][start_x] = "|"
    elif start_neighbours == {(start_x, start_y - 1), (start_x + 1, start_y)}:
        lines[start_y][start_x] = "L"
    elif start_neighbours == {(start_x, start_y + 1), (start_x - 1, start_y)}:
        lines[start_y][start_x] = "7"
    elif start_neighbours == {(start_x, start_y - 1), (start_x - 1, start_y)}:
        lines[start_y][start_x] = "J"
    elif start_neighbours == {(start_x, start_y + 1), (start_x + 1, start_y)}:
        lines[start_y][start_x] = "F"
    else:
        raise ValueError(
            f"Unknown neighbours: {start_neighbours}, start pos: {start_pos}"
        )

    inside = False
    corner = ""
    res = 0

    # simpler solution than mine
    # as my initial idea, count the vertical bars each row from left to right, and
    # flip a boolean flag between inside<->outside if a vertical bar is crossed, and store every
    # non-loop cell based on the state of the flag
    # However, this is the trick I didn't think of:
    #     L-----J wall segments DO NOT change the state of the flag
    #     L-----7 wall segments DO change the state of the flag
    #     F-----J wall segments DO change the state of the flag
    #     F-----7 wall segments DO NOT change the state of the flag

    inside_cells = set()
    for y in range(height):
        for x in range(width):
            if (x, y) not in main_loop and inside:
                inside_cells.add((x, y))
                res += 1

            if (x, y) in main_loop:
                tile = lines[y][x]
                if tile in "LF":
                    corner = tile
                elif tile == "J":
                    if corner == "L":
                        pass
                    elif corner == "F":
                        inside = not inside
                    corner = ""
                elif tile == "7":
                    if corner == "L":
                        inside = not inside
                    elif corner == "F":
                        pass
                    corner = ""
                elif (tile == "-") and (corner != ""):
                    pass
                elif tile == "|":
                    inside = not inside

    for y in range(height):
        for x in range(width):
            char_to_print = "."
            if (x, y) in main_loop:
                char_to_print = lines[y][x]
            elif (x, y) in inside_cells:
                char_to_print = "I"
            print(char_to_print, end="")
        print()

    print("len(inside_cells)", len(inside_cells))
    print("res", res)


if __name__ == "__main__":
    # sandbox()
    sandbox_2()
    # sandbox_reddit()
    # print("Part 1:", part_1())
