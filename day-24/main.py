from pathlib import Path


Vector = tuple[int, int, int]


def parse_input(filename: str) -> list[tuple[Vector, Vector]]:
    lines = Path(filename).read_text().splitlines()

    result = []

    for line in lines:
        ps, vs = line.split(" @ ")
        p = tuple(map(int, ps.split(",")))
        v = tuple(map(int, vs.split(",")))
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

            # print("Hailstone A:", p1, "@", v1)
            # print("Hailstone B:", p2, "@", v2)

            p1x, p1y, _ = p1
            v1x, v1y, _ = v1
            c1 = v1y * p1x - v1x * p1y

            p2x, p2y, _ = p2
            v2x, v2y, _ = v2
            c2 = v2y * p2x - v2x * p2y

            det = v1x * v2y - v1y * v2x
            if det == 0:
                # print("Parallel")
                # print()
                continue

            x = (v1x * c2 - v2x * c1) / det
            y = (v1y * c2 - v2y * c1) / det

            t1 = (x - p1x) / v1x
            t2 = (x - p2x) / v2x

            # if min_coord <= x <= max_coord and min_coord <= y <= max_coord:
            #     print("Intersection inside:", x, y)
            # else:
            #     print("Intersection outside:", x, y)

            # print("t1:", t1)
            # print("t2:", t2)

            # print()

            if (
                min_coord <= x <= max_coord
                and min_coord <= y <= max_coord
                and t1 >= 0
                and t2 >= 0
            ):
                result += 1

    return result


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
