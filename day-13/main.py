from collections.abc import Iterable
from typing import Optional


def read_patterns(filename: str) -> Iterable[list[str]]:
    buffer = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                yield buffer
                buffer = []
            else:
                buffer.append(line)

    if len(buffer) > 0:
        yield buffer


def different_indexes(str1: str, str2: str) -> list[int]:
    assert len(str1) == len(str2)

    return [i for i in range(len(str1)) if str1[i] != str2[i]]


def find_horizontal_mirror(pattern: list[str]) -> Optional[int]:
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i + 1]:
            is_mirror = True

            upper_side = reversed(pattern[:i])
            lower_side = pattern[i + 2 :]
            for row_up, row_down in zip(upper_side, lower_side):
                if row_up != row_down:
                    is_mirror = False
                    break

            if is_mirror:
                return i

    return None


def find_horizontal_smudge_mirror(pattern: list[str]) -> Optional[int]:
    for i in range(len(pattern) - 1):
        diff = different_indexes(pattern[i], pattern[i + 1])
        if len(diff) < 2:
            smudge_found = len(diff) == 1
            is_mirror = True

            upper_side = reversed(pattern[:i])
            lower_side = pattern[i + 2 :]
            for row_up, row_down in zip(upper_side, lower_side):
                diff2 = different_indexes(row_up, row_down)
                if len(diff2) > 1:
                    is_mirror = False
                    break
                elif len(diff2) == 1:
                    if not smudge_found:
                        smudge_found = True
                    else:
                        is_mirror = False
                        break

            if is_mirror and smudge_found:
                return i

    return None


def transpose(pattern: list[str]) -> list[str]:
    return ["".join(row) for row in zip(*pattern)]


def part_1():
    patterns = list(read_patterns("input.txt"))

    sum = 0

    for pattern in patterns:
        horizontal_mirror = find_horizontal_mirror(pattern)
        if horizontal_mirror is not None:
            sum += (horizontal_mirror + 1) * 100
        else:
            vertical_mirror = find_horizontal_mirror(transpose(pattern))
            assert vertical_mirror is not None
            sum += vertical_mirror + 1

    return sum


def part_2():
    patterns = list(read_patterns("input.txt"))

    sum = 0

    for pattern in patterns:
        horizontal_mirror = find_horizontal_smudge_mirror(pattern)
        if horizontal_mirror is not None:
            sum += (horizontal_mirror + 1) * 100
        else:
            vertical_mirror = find_horizontal_smudge_mirror(transpose(pattern))
            assert vertical_mirror is not None
            sum += vertical_mirror + 1

    return sum


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
