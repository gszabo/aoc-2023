from itertools import combinations
from pathlib import Path

import re


def read_input(filename: str) -> list[tuple[str, list[int]]]:
    lines = Path(filename).read_text().splitlines()
    return [
        ((parts := line.split())[0], list(map(int, parts[1].split(","))))
        for line in lines
    ]


def calc_groups(record: str) -> list[int]:
    result = []

    counter = 0
    for char in record:
        if char == "#":
            counter += 1
        elif counter > 0:
            result.append(counter)
            counter = 0

    return result


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


def part_1_other():
    # source
    # reddit: https://www.reddit.com/r/adventofcode/comments/18ge41g/comment/kd6636r/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # github: https://github.com/weibell/AoC2023-python/blob/main/day12/part1.py

    def is_valid_arrangement(record: str, expected_group_sizes: list[int]) -> bool:
        actual_groups = re.findall(r'#+', record)
        actual_group_sizes = list(map(len, actual_groups))
        return actual_group_sizes == expected_group_sizes

    with open('input.txt') as f:
        input_data = f.read().splitlines()

    total_arrangements = 0
    for line in input_data:
        record, groups = line.split(' ')
        group_sizes = list(map(int, groups.split(',')))

        total_springs = sum(group_sizes)
        unassigned_springs = total_springs - record.count('#')
        unassigned_positions = [i for i, char in enumerate(record) if char == '?']

        arrangements_counter = 0
        for assignment in combinations(unassigned_positions, unassigned_springs):
            new_record = list(record)
            for position in assignment:
                new_record[position] = '#'
            if is_valid_arrangement(''.join(new_record), group_sizes):
                arrangements_counter += 1

        total_arrangements += arrangements_counter

    return total_arrangements


def part_2():
    puzzle_input = read_input("input_sample.txt")

    sum = 0

    for record, desired_groups in puzzle_input:
        unfolded_record = "?".join([record] * 5)
        unfolded_groups = desired_groups * 5
        sum += count_possible_combinations(unfolded_record, unfolded_groups)

    return sum


if __name__ == "__main__":
    print("Part 1:", part_1())
    # print("Part 1:", part_1_other())
    # print("Part 2:", part_2())
