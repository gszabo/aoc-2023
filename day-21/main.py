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


def print_reachable_field(
    field: dict[Coord, str], reachable: set[Coord], step: int, width: int, height: int
):
    with open(f"reachable_{step+1}.txt", "w") as f:
        for y in range(height):
            for x in range(width):
                if (x, y) in reachable:
                    f.write("O")
                else:
                    f.write(field[(x, y)])
            f.write("\n")


def part_2():
    # The given 26501365 steps is not an arbitrary number.
    # 26501365 = 202300 * 131 + 65
    # where the input is a 131x131 square and the starting point is exactly in the middle,
    # so in 26501365 steps we can walk 65 steps to the edge of the garden + 202300 times walk the length or width of the garden.
    #
    # The solution here is to find the number of reachable squares for n * 131 + 65 steps, where n is small, by
    # walking the garden. Then we can fit a quadratic curve to the data and calculate the value of the curve at
    # the desired n=202300. It is unclear yet why a quadratic curve fits the problem, what special properties
    # of the input contribute to this.
    #
    # An other approach that examines the input more deeply can be found here:
    # - https://www.reddit.com/r/adventofcode/comments/18nol3m/2023_day_21_a_geometric_solutionexplanation_for/
    # - https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
    #
    # Another, analytical approach that only assumes it is a pseudo-periodic function:
    # - https://www.reddit.com/r/adventofcode/comments/18nxp7x/2023_day_21_part_2_analytical_solution/
    # - https://colab.research.google.com/drive/16yAGjSGyvHuAurfht0yUv18eY7T207yR

    data = parse_input("input.txt")
    step_count = 2000

    field = data["field"]
    start = data["start"]
    width = data["width"]
    height = data["height"]

    # cache = {}

    def reachable_in_n_step(origin: Coord, n: int) -> set[Coord]:
        # For some reason this cache doesn't work. The computation based on this cache gives wrong answer
        # to part 1, even though first few numbers are correct.
        # This error made me unable to fit a quadratic curve to the data. Leaving the debugging for another day.

        # origin_x, origin_y = origin
        # mapped_x, mapped_y = origin_x % width, origin_y % height
        # if (mapped_x, mapped_y) in cache:
        #     deltas = cache[(mapped_x, mapped_y)]
        #     return set((origin_x + dx, origin_y + dy) for dx, dy in deltas)

        reachable = {origin}

        for _ in range(n):
            new_reachable = set()

            for x, y in reachable:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    new_x = x + dx
                    new_y = y + dy
                    if field[(new_x % width, new_y % height)] == ".":
                        new_reachable.add((new_x, new_y))

            reachable = new_reachable

        # cache[(mapped_x, mapped_y)] = set((x2 - origin_x, y2 - origin_y) for x2, y2 in reachable)

        return reachable

    reachables = {0: {start}, 1: reachable_in_n_step(start, 1)}
    shells = {**reachables}

    print(0, len(reachables[0]), sep=",")
    print(1, len(reachables[1]), sep=",")

    for i in range(2, step_count):
        parity = i % 2

        new_reachable = set()
        for o in shells[parity]:
            new_reachable |= reachable_in_n_step(o, 2)

        new_shell = new_reachable - reachables[parity]

        reachables[parity] |= new_shell
        shells[parity] = new_shell

        print(i, len(reachables[parity]), sep=",")

    # post processing steps for the printed csv:
    # - offset the step column by -65
    # - only use those rows where the new step column is divisible by 131
    # - fit an ax^2 + bx + c curve to the remaining rows
    # - calculate the value of the curve at x = (26501365 - 65) / 131

    # a = 14655, b = 14775, c = 3720
    # f(x) = 14655x^2 + 14775x + 3720
    # f(202300) = 599763113936220


if __name__ == "__main__":
    # print("Part 1:", part_1())
    part_2()
    # print("Part 2:", part_2())
