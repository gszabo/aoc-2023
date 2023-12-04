from operator import attrgetter


def read_input():
    # read input.txt into a 140x140 matrix
    with open("input.txt", "r") as f:
        data = f.readlines()
        data = [list(x.strip()) for x in data]
        return data


DATA = read_input()
WIDTH = len(DATA[0])
HEIGHT = len(DATA)


def get_value_at(x: int, y: int) -> str:
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        return DATA[y][x]
    else:
        return "."


class NumberWrapper:
    # compare by identity, not by value,
    # because the same "engine part number" can appear multiple times in the grid
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(id(self))


def build_numbers_map() -> dict[tuple[int, int], NumberWrapper]:
    # build a map of coordinates to numbers
    # key: (x, y) tuple
    # value: number at that coordinate, with a wrapper because we need to compare these numbers by identity
    # if there's a multi-digit number at a coordinate, store that number to all the coordinates it covers
    numbers_map = {}

    for y in range(HEIGHT):
        x = 0
        while x < WIDTH:
            value = get_value_at(x, y)
            if value.isdigit():
                i = 1
                while get_value_at(x + i, y).isdigit():
                    i += 1
                number = NumberWrapper(
                    int("".join([get_value_at(x + j, y) for j in range(i)]))
                )
                for j in range(i):
                    numbers_map[(x + j, y)] = number
                x += i
            else:
                x += 1

    return numbers_map


def build_symbols_map() -> dict[tuple[int, int], str]:
    # build a map of coordinates to symbols
    # key: (x, y) tuple
    # value: symbol at that coordinate
    symbols_map = {}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            value = get_value_at(x, y)
            if not value.isdigit() and value != ".":
                symbols_map[(x, y)] = value

    return symbols_map


def part_1():
    numbers_map = build_numbers_map()
    symbols_map = build_symbols_map()

    numbers_adjacent_to_symbols = set()

    # iterate over symbols and check if there is any adjacent number (even diagonally)
    # if there is, add that number to the set
    for x, y in symbols_map:
        adjacent_coords = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
        for coord in adjacent_coords:
            if coord in numbers_map:
                numbers_adjacent_to_symbols.add(numbers_map[coord])

    return sum(map(attrgetter("value"), numbers_adjacent_to_symbols))

def part_2():
    numbers_map = build_numbers_map()
    symbols_map = build_symbols_map()

    # iterate over '*' symbols and check if it is adjecent to exactly 2 numbers
    sum = 0
    for x, y in symbols_map:
        if symbols_map[(x, y)] != "*":
            continue

        adjacent_coords = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
        adjacent_numbers = {numbers_map[coord] for coord in adjacent_coords if coord in numbers_map}
        if len(adjacent_numbers) == 2:
            one, two = adjacent_numbers
            sum += one.value * two.value

    return sum


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
