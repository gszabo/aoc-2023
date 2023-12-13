from itertools import groupby
from pathlib import Path


def read_input(filename: str) -> list[tuple[str, list[int]]]:
    lines = Path(filename).read_text().splitlines()
    return [
        ((parts := line.split())[0], list(map(int, parts[1].split(","))))
        for line in lines
    ]


def calc_groups(record: str) -> list[int]:
    return [len(list(group)) for char, group in groupby(record) if char == "#"]


def count_possible_combinations(record: str, desired_groups: list[int]) -> int:
    def inner_count(text: str) -> int:
        groups = calc_groups(text)
        if "?" not in text:
            return 1 if groups == desired_groups else 0

        first_joker_index = text.index("?")
        already_fixed_groups = calc_groups(text[:first_joker_index])
        if len(already_fixed_groups) > len(desired_groups):
            return 0
        for i in range(len(already_fixed_groups)):
            if already_fixed_groups[i] > desired_groups[i]:
                return 0

        return inner_count(text.replace("?", "#", 1)) + inner_count(text.replace("?", ".", 1))

    return inner_count(record)



def part_1():
    puzzle_input = read_input("input.txt")

    sum = 0

    for record, desired_groups in puzzle_input:
        sum += count_possible_combinations(record, desired_groups)

    return sum


def part_2():
    puzzle_input = read_input("input_sample.txt")

    sum = 0

    for record, desired_groups in puzzle_input:
        unfolded_record = "?".join([record] * 5)
        unfolded_groups = desired_groups * 5
        sum += count_possible_combinations(unfolded_record, unfolded_groups)

    return sum


if __name__ == "__main__":
    # print("Part 1:", part_1())
    print("Part 2:", part_2())
