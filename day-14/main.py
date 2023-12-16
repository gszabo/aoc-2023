from copy import deepcopy
from pathlib import Path


def read_input(filename: str) -> list[str]:
    return Path(filename).read_text().splitlines()


def part_1():
    lines = read_input("input.txt")

    width = len(lines[0])
    height = len(lines)

    sum = 0

    for j in range(width):
        next_collect_position = 0
        for i in range(height):
            ch = lines[i][j]
            if ch == "#":
                next_collect_position = i + 1
            elif ch == "O":
                sum += height - next_collect_position
                next_collect_position += 1

    return sum


def total_north_load(matrix: list[list[str]]) -> int:
    width = len(matrix[0])
    height = len(matrix)

    sum = 0

    for j in range(width):
        for i in range(height):
            ch = matrix[i][j]
            if ch == "O":
                sum += height - i

    return sum


def north(matrix: list[list[str]]) -> list[list[str]]:
    width = len(matrix[0])
    height = len(matrix)

    matrix = deepcopy(matrix)

    for j in range(width):
        next_collect_position = 0
        for i in range(height):
            ch = matrix[i][j]
            if ch == "#":
                next_collect_position = i + 1
            elif ch == "O":
                matrix[next_collect_position][j] = "O"
                if i != next_collect_position:
                    # if the O round rock actually moved then replace the original place with .
                    matrix[i][j] = "."
                next_collect_position += 1

    return matrix


def west(matrix: list[list[str]]) -> list[list[str]]:
    width = len(matrix[0])
    height = len(matrix)

    matrix = deepcopy(matrix)

    for i in range(height):
        next_collect_position = 0
        for j in range(width):
            ch = matrix[i][j]
            if ch == "#":
                next_collect_position = j + 1
            elif ch == "O":
                matrix[i][next_collect_position] = "O"
                if j != next_collect_position:
                    # if the O round rock actually moved then replace the original place with .
                    matrix[i][j] = "."
                next_collect_position += 1

    return matrix


def south(matrix: list[list[str]]) -> list[list[str]]:
    width = len(matrix[0])
    height = len(matrix)

    matrix = deepcopy(matrix)

    for j in range(width):
        next_collect_position = height - 1
        for i in reversed(range(height)):
            ch = matrix[i][j]
            if ch == "#":
                next_collect_position = i - 1
            elif ch == "O":
                matrix[next_collect_position][j] = "O"
                if i != next_collect_position:
                    # if the O round rock actually moved then replace the original place with .
                    matrix[i][j] = "."
                next_collect_position -= 1

    return matrix


def east(matrix: list[list[str]]) -> list[list[str]]:
    width = len(matrix[0])
    height = len(matrix)

    matrix = deepcopy(matrix)

    for i in range(height):
        next_collect_position = width - 1
        for j in reversed(range(width)):
            ch = matrix[i][j]
            if ch == "#":
                next_collect_position = j - 1
            elif ch == "O":
                matrix[i][next_collect_position] = "O"
                if j != next_collect_position:
                    # if the O round rock actually moved then replace the original place with .
                    matrix[i][j] = "."
                next_collect_position -= 1

    return matrix


def cycle(matrix: list[list[str]]) -> list[list[str]]:
    return east(south(west(north(matrix))))


def print_matrix(matrix: list[list[str]]):
    for row in matrix:
        print("".join(row))


def part_2():
    matrix = [list(line) for line in read_input("input.txt")]
    total_cycle_count = 1000000000

    matrices = [matrix]

    loop_found = False
    loop_start_index = None
    loop_end_index = None

    for i in range(total_cycle_count):
        new_matrix = cycle(matrices[-1])
        for j, m in enumerate(matrices):
            if new_matrix == m:
                print(f"Index {j} equals index {i+1}")
                loop_start_index = j
                # i + 1 is the new_matrix insertion index because the list starts with one item
                loop_end_index = i + 1
                loop_found = True
                break

        matrices.append(new_matrix)

        if loop_found:
            break

    if not loop_found:
        # most likely this will not happen as the cycle count above is a very large number
        return total_north_load(matrices[-1])

    loop_len = loop_end_index - loop_start_index

    target_matrix = matrices[
        (total_cycle_count - loop_start_index) % loop_len + loop_start_index
    ]

    return total_north_load(target_matrix)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
