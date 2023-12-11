from pathlib import Path


def expand_input():
    rows_to_duplicate = []
    columns_to_duplicate = []

    lines = Path("input.txt").read_text().splitlines()

    width = len(lines[0])
    height = len(lines)

    for row in range(height):
        if lines[row] == "." * width:
            rows_to_duplicate.append(row)

    for column in range(width):
        if all([lines[row][column] == "." for row in range(height)]):
            columns_to_duplicate.append(column)

    print("Rows", rows_to_duplicate)
    print("Columns", columns_to_duplicate)

    expanded_lines = []
    for row in range(height):
        expanded_line = ""

        for column in range(width):
            expanded_line += lines[row][column]
            if column in columns_to_duplicate:
                expanded_line += lines[row][column]

        expanded_lines.append(expanded_line)
        if row in rows_to_duplicate:
            expanded_lines.append(expanded_line)

    with open("expanded_input.txt", "w") as f:
        for line in expanded_lines:
            f.write(line + "\n")


def collect_emtpy_rows(lines: list[str]) -> list[int]:
    width = len(lines[0])
    return [row_number for row_number, line in enumerate(lines) if line == "." * width]


def collect_empty_columns(lines: list[str]) -> list[tuple[int, int]]:
    width = len(lines[0])
    height = len(lines)

    return [
        col
        for col in range(width)
        if all([lines[row][col] == "." for row in range(height)])
    ]


def collect_coordinates(lines: list[str]) -> list[tuple[int, int]]:
    width = len(lines[0])
    height = len(lines)

    return [
        (column, row)
        for row in range(height)
        for column in range(width)
        if lines[row][column] == "#"
    ]


def part_1():
    lines = Path("expanded_input.txt").read_text().splitlines()
    coordinates = collect_coordinates(lines)

    sum = 0

    for i in range(len(coordinates) - 1):
        for j in range(i + 1, len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            distance = abs(x1 - x2) + abs(y1 - y2)
            sum += distance

    return sum


def part_2():
    lines = Path("input.txt").read_text().splitlines()

    empty_rows = collect_emtpy_rows(lines)
    empty_columns = collect_empty_columns(lines)
    coordinates = collect_coordinates(lines)

    sum = 0

    for i in range(len(coordinates) - 1):
        for j in range(i + 1, len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            distance = abs(x1 - x2) + abs(y1 - y2)

            empty_cols_in_between = len(
                [col for col in empty_columns if min(x1, x2) < col < max(x1, x2)]
            )
            empty_rows_in_between = len(
                [row for row in empty_rows if min(y1, y2) < row < max(y1, y2)]
            )

            distance += (empty_cols_in_between + empty_rows_in_between) * (
                1_000_000 - 1
            )

            sum += distance

    return sum


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
