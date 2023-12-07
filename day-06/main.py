# Time:        46828479
# Distance:   347152214061471

from math import sqrt, ceil, floor
from operator import mul
from functools import reduce



def count_possible_solutions(time: int, distance: int) -> int:
    det = time * time - 4 * distance

    x_1 = (time - sqrt(det)) / 2
    x_2 = (time + sqrt(det)) / 2

    first_good_integer = floor(x_1 + 1)
    last_good_integer = ceil(x_2 - 1)

    return last_good_integer - first_good_integer + 1


def part_1():
    times = [46, 82, 84, 79]
    distances = [347, 1522, 1406, 1471]

    return reduce(
        mul,
        (
            count_possible_solutions(time, distance)
            for time, distance in zip(times, distances)
        ),
        1,
    )


def part_2():
    time = 46828479
    distance = 347152214061471
    return count_possible_solutions(time, distance)


if __name__ == "__main__":
    print("Part 1", part_1())
    print("Part 2", part_2())
