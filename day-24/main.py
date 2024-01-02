from decimal import Decimal
from pathlib import Path

from linalg import solve_2x2


Vector = tuple[Decimal, Decimal, Decimal]


def parse_input(filename: str) -> list[tuple[Vector, Vector]]:
    lines = Path(filename).read_text().splitlines()

    result = []

    for line in lines:
        ps, vs = line.split(" @ ")
        p = tuple(map(Decimal, ps.split(",")))
        v = tuple(map(Decimal, vs.split(",")))
        result.append((p, v))

    return result


def part_1():
    data = parse_input("input.txt")

    min_coord = 200000000000000
    max_coord = 400000000000000

    result = 0

    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            p1, v1 = data[i]
            p2, v2 = data[j]

            p1x, p1y, _ = p1
            v1x, v1y, _ = v1

            p2x, p2y, _ = p2
            v2x, v2y, _ = v2

            # Path equation for a line passing through a point (x0, y0) with direction vector (v_x, v_y):
            # (x - x0) / v_x = (y - y0) / v_y, or
            # v_y * x - v_x * y = v_y * x0 - v_x * y0

            # Finding the intersection of two lines is solving a system of two linear equations:
            # v1_y * x - v1_x * y = v1_y * x1 - v1_x * y1
            # v2_y * x - v2_x * y = v2_y * x2 - v2_x * y2

            # Calculating the right hand side of the equations:
            c1 = v1y * p1x - v1x * p1y
            c2 = v2y * p2x - v2x * p2y

            try:
                x, y = solve_2x2(
                    [
                        [v1y, -v1x],
                        [v2y, -v2x],
                    ],
                    [c1, c2],
                )

                # Calculating the "time component", ie. when the hailstones happen to be at the intersection
                # If ti < 0, the hailstone was at the intersection in the past.
                t1 = (x - p1x) / v1x
                t2 = (x - p2x) / v2x

                if (
                    min_coord <= x <= max_coord
                    and min_coord <= y <= max_coord
                    and t1 >= 0
                    and t2 >= 0
                ):
                    result += 1
            except ValueError:
                # print("Parallel")
                # print()
                continue

    return result


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
