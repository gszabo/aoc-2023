from functools import cache
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

        return inner_count(text.replace("?", "#", 1)) + inner_count(
            text.replace("?", ".", 1)
        )

    return inner_count(record)


def possible_group_prefix(record: str) -> int:
    result = 0
    for ch in record:
        if ch == "#" or ch == "?":
            result += 1
        else:
            break
    return result


# This is my attempt at optimizing the original `count_possible_combinations` function
# hoping it has better cache-ability and speed.
# For @cache to work, the groups argument has to be a tuple instead of a list,
# because the list type is unhashable.
@cache
def count_arrangements(record: str, groups: tuple[int, ...]) -> int:
    if record == "":
        return 1 if len(groups) == 0 else 0

    if len(groups) == 0:
        return 1 if record.find("#") == -1 else 0

    first_group, other_groups = groups[0], groups[1:]

    # removing .s from the beginning of the record, because they are fixed,
    # cannot be changed and does not count into any of the groups
    stripped_record = record.lstrip(".")

    possible_first_group = possible_group_prefix(stripped_record)
    possible_first_group_chars = stripped_record[:possible_first_group]

    if possible_first_group < first_group:
        # if the possible first group is all ? then there may still be a chance to find a good arrangement
        # by using . for every ? in the first possible group and checking if later groups can satisfy the requirements
        # but if there's at least one # in the possible first group, then it cannot all be ., so there has to be a
        # group here and the size of this group cannot satisfy the requirement for the first group size
        if "#" in possible_first_group_chars:
            return 0
        else:
            return count_arrangements(stripped_record[possible_first_group:], groups)

    if possible_first_group == first_group:
        # Here first_group == possible_first_group <= len(stripped_record)
        # because if len(stripped_record) < first_group was the case,
        # then possible_first_group could not be equal to first_group as it cannot be longer than the string.

        if first_group == len(stripped_record):
            if len(groups) == 1:
                # exact match
                return 1
            else:
                # exact match for first group, but there has to be other groups
                return 0
        elif stripped_record[first_group] == "#":
            # too large group
            return 0
        else:
            if "#" in possible_first_group_chars:
                # the first group has to be the first possible group
                return count_arrangements(
                    stripped_record[first_group + 1 :], other_groups
                )
            else:
                # one case is when the first group is the first possible group
                # other case is when we completely jump over this possible group (all of it is ? in the else branch)
                return count_arrangements(
                    stripped_record[first_group + 1 :], other_groups
                ) + count_arrangements(stripped_record[first_group:], groups)

    if possible_first_group > first_group:
        first_letter = stripped_record[0]
        if first_letter != "#" and first_letter != "?":
            raise ValueError(f"Unexpected first letter '{first_letter}'")

        letter_after_group = stripped_record[first_group]
        if first_letter == "#":
            # the group has to start here
            if letter_after_group == "#":
                # too large group
                return 0
            else:
                # skip group + ? char afterwards that has to be a separator .
                return count_arrangements(
                    stripped_record[first_group + 1 :], other_groups
                )
        elif first_letter == "?":
            if letter_after_group == "#":
                # first letter has to be "."
                return count_arrangements(stripped_record[1:], groups)
            else:
                dot_case = count_arrangements(stripped_record[1:], groups)
                hash_case = count_arrangements(
                    stripped_record[first_group + 1 :], other_groups
                )
                return dot_case + hash_case

    raise ValueError(
        f"Unexpected first group case: possible={possible_first_group} needed={first_group}"
    )


def sandbox():
    puzzle_input = read_input("input_sample.txt")

    for record, desired_groups in puzzle_input:
        arrangement_count = count_arrangements(record, desired_groups)
        # print()
        print(record, desired_groups, arrangement_count)


def part_1():
    puzzle_input = read_input("input.txt")

    sum = 0

    for record, desired_groups in puzzle_input:
        sum += count_possible_combinations(record, desired_groups)

    return sum


def part_1_optimized_by_me():
    puzzle_input = read_input("input.txt")

    sum = 0

    for record, desired_groups in puzzle_input:
        sum += count_arrangements(record, tuple(desired_groups))

    return sum


def part_1_other():
    # source
    # reddit: https://www.reddit.com/r/adventofcode/comments/18ge41g/comment/kd6636r/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # github: https://github.com/weibell/AoC2023-python/blob/main/day12/part1.py

    def is_valid_arrangement(record: str, expected_group_sizes: list[int]) -> bool:
        actual_groups = re.findall(r"#+", record)
        actual_group_sizes = list(map(len, actual_groups))
        return actual_group_sizes == expected_group_sizes

    with open("input.txt") as f:
        input_data = f.read().splitlines()

    total_arrangements = 0
    for line in input_data:
        record, groups = line.split(" ")
        group_sizes = list(map(int, groups.split(",")))

        total_springs = sum(group_sizes)
        unassigned_springs = total_springs - record.count("#")
        unassigned_positions = [i for i, char in enumerate(record) if char == "?"]

        arrangements_counter = 0
        for assignment in combinations(unassigned_positions, unassigned_springs):
            new_record = list(record)
            for position in assignment:
                new_record[position] = "#"
            if is_valid_arrangement("".join(new_record), group_sizes):
                arrangements_counter += 1

        # DEBUG my algorithm, find the input where the answer is wrong.
        # my_implementation_counter = count_arrangements(record, group_sizes)
        # if arrangements_counter != my_implementation_counter:
        #     print("Mismatch", record, group_sizes, arrangements_counter, my_implementation_counter)

        total_arrangements += arrangements_counter

    return total_arrangements


def part_2():
    puzzle_input = read_input("input.txt")

    sum = 0

    for record, desired_groups in puzzle_input:
        unfolded_record = "?".join([record] * 5)
        unfolded_groups = desired_groups * 5
        # clearing the cache between inputs makes it faster
        count_arrangements.cache_clear()
        sum += count_arrangements(unfolded_record, tuple(unfolded_groups))
        # print(count_arrangements.cache_info())



    return sum


if __name__ == "__main__":
    # sandbox()
    # print("Part 1:", part_1())
    # print("Part 1:", part_1_other())
    print("Part 1:", part_1_optimized_by_me())
    print("Part 2:", part_2())
