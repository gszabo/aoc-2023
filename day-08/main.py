from itertools import cycle

STEP_LINE = "LRRLRLRRRLLRLRRRLRLLRLRLRRLRLRRLRRLRLRLLRRRLRRLLRRRLRRLRRRLRRLRLRLLRRLRLRRLLRRRLLLRRRLLLRRLRLRRLRLLRRRLRRLRRRLRRLLRRRLRRRLRRRLRLRRLRLRRRLRRRLRRLRLRRLLRRRLRRLLRRLRRLRLRLRRRLRLLRRRLRRLRRRLLRRLLLLLRRRLRRLLLRRRLRRRLRRLRLLLLLRLRRRLRRRLRLRRLLLLRLRRRLLRRRLRRRLRLRLRRLRRLRRLRLRLLLRLRRLRRLRRRLRRRLLRRRR"


def read_map():
    # read input.txt from the 3rd line
    # each line looks like this: "RBX = (TMF, KTP)"
    # put each line into a dict, for the exmple above, it will be:
    # {"RBX": {"L": "TMF", "R": "KTP"}}
    # return the dict

    with open("input.txt") as f:
        lines = f.readlines()[2:]
        result = {}
        for line in lines:
            line = line.strip()
            key, value = line.split(" = ")
            value = value[1:-1]
            value = value.split(", ")
            result[key] = {"L": value[0], "R": value[1]}
        return result


def least_common_multiple(numbers: list[int]) -> int:
    # return the least common multiple of the numbers
    # hint: https://en.wikipedia.org/wiki/Least_common_multiple#Using_the_greatest_common_divisor

    # assuming all numbers are positive integers

    def gcd(a: int, b: int) -> int:
        if b == 0:
            return a
        return gcd(b, a % b)

    def lcm(a: int, b: int) -> int:
        return a * b // gcd(a, b)

    result = 1
    for number in numbers:
        result = lcm(result, number)

    return result


def part_1():
    puzzle_map = read_map()
    steps = cycle(STEP_LINE)

    current = "AAA"
    for i, step in enumerate(steps):
        current = puzzle_map[current][step]
        if current == "ZZZ":
            return i + 1


def part_2():
    puzzle_map = read_map()
    steps = cycle(STEP_LINE)

    def calculate_period(start: str) -> int:
        current = start
        for i, step in enumerate(steps):
            current = puzzle_map[current][step]
            if current.endswith("Z"):
                return i + 1

    start_locations = list(filter(lambda x: x.endswith("A"), puzzle_map.keys()))
    periods = list(map(calculate_period, start_locations))
    return least_common_multiple(periods)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
