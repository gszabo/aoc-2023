from fractions import Fraction
from pathlib import Path

from linalg import solve_2x2, solve_4x4


Vector = tuple[Fraction, Fraction, Fraction]


def parse_input(filename: str) -> list[tuple[Vector, Vector]]:
    lines = Path(filename).read_text().splitlines()

    result = []

    for line in lines:
        ps, vs = line.split(" @ ")
        # Using Fraction to arrive at exact integer results.
        # Using ints result in wrong answer, because of the divisions resulting in floats during the Gauss elimination in part 2.
        # Using Decimal gets very close to the correct integer result (a basic rounding is enough to get the correct answer),
        # but it's still not exact. I don't know why.
        p = tuple(map(Fraction, ps.split(",")))
        v = tuple(map(Fraction, vs.split(",")))
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
    # Rock's initial position: (px, py, pz)
    # Rock's initial velocity: (vx, vy, vz)

    # First 5 rows are enough to set up the equation system.
    # As a first step, we need to create a system of 4 linear equations for the x, y variables: px, py, vx, vy
    # Let t1, t2, t3, ... denote the time when the first, second, third, ... hailstone is hit by the rock.
    #
    # At these times, the rock is at the same position as the hailstone, so we can write the following equations for the first hailstone:
    #   ( I)  px + vx * t1 = p1x + v1x * t1
    #   (II)  py + vy * t1 = p1y + v1y * t1
    #
    # Generally for the ith hailstone:
    #   (2i-1)  px + vx * ti = pi_x + vi_x * ti
    #   (2i)    py + vy * ti = pi_y + vi_y * ti
    #
    # So far all the ti variables are unknown, and the system is not linear, but we can rearrange the equations to get a linear system.
    #
    # Rearranging (2i-1) and (2i) for ti:
    #   ti = (pi_x - px) / (vx - vi_x) = (pi_y - py) / (vy - vi_y)
    #
    # Rearranging to get rid of divisions:
    #  (i) vi_y * px - vi_x * py + py * vx - px * vy - pi_y * vx + pi_x * vy = pi_x * vi_y - pi_y * vi_x
    #
    # On the left hand side this still contains a non-linear term (py * vx - px * vy), but it is the same term for all i = 1, 2, 3, ...
    #
    # We can create a new equation system by eg. subtracting (2), (3), (4), ... from (1), ie. (1) - (i), i = 2, 3, 4, ...
    #  (i-1) (v1_y - vi_y) * px + (vi_x - v1_x) * py + (pi_y - p1_y) * vx - (p1_x - pi_x) * vy = p1_x * v1_y - p1_y * v1_x - pi_x * vi_y + pi_y * vi_x
    #
    # So by grabbing the first 5 hailstones from the input data, writing the equations by eliminating ti and then doing the
    # above substractions ((1) - (i), for i = 2, 3, 4, 5), we get a system of 4 linear equations for the 4 unknowns: px, py, vx, vy.
    # We can solve this system using Gaussian elimination and get the values for px, py, vx, vy.

    data = parse_input("input.txt")

    m = []
    b = []

    p1x, p1y, p1z, v1x, v1y, v1z = [*data[0][0], *data[0][1]]
    p2x, _, p2z, v2x, _, v2z = [*data[1][0], *data[1][1]]

    for i in range(1, 5):
        pix, piy, _, vix, viy, _ = [*data[i][0], *data[i][1]]
        m.append([v1y - viy, vix - v1x, piy - p1y, p1x - pix])
        b.append(p1x * v1y - p1y * v1x - pix * viy + piy * vix)

    px, py, vx, vy = solve_4x4(m, b)

    # Now that we have all variables for x and y coordinates,
    # we can use the first two hailstones to calculate the z variables:
    #   ( I)  pz + vz * t1 = p1z + v1z * t1
    #   (II)  pz + vz * t2 = p2z + v2z * t2
    # t1 and t2 are known values based on the solution above:
    #   t1 = (p1x - px) / (vx - v1x)
    #   t2 = (p2x - px) / (vx - v2x)
    # So we need to solve a system of two linear equations of two variables.

    t1 = (p1x - px) / (vx - v1x)
    t2 = (p2x - px) / (vx - v2x)

    pz, vz = solve_2x2(
        [
            [1, t1],
            [1, t2],
        ],
        [p1z + v1z * t1, p2z + v2z * t2],
    )

    print(px, py, pz, vx, vy, vz)
    return px + py + pz


def sandbox():
    # this was used to try to understand the inner workings of the AI-generated Gaussian elimination code
    # at the time of writing the code does not do what I expect it to do, but it works
    m = [
        [2, 1, 6, 1],
        [3, 0, 12, -1],
        [3, 1, 18, 7],
        [6, 3, 6, -1],
    ]
    b = [44, 35, 38, 164]
    print(solve_4x4(m, b))


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
    # sandbox()
