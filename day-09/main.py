def get_diffs(numbers: list[int]) -> list[int]:
    return [b - a for a, b in zip(numbers, numbers[1:])]


def is_zero(number: int) -> bool:
    return number == 0


def predict_next_value_for_history(history: list[int]) -> int:
    diff_lists = [history]
    while True:
        next_list = get_diffs(diff_lists[-1])
        diff_lists.append(next_list)
        if all(map(is_zero, next_list)):
            break

    predicted_value = 0
    for diff_list in reversed(diff_lists):
        predicted_value += diff_list[-1]

    return predicted_value


def predict_previous_value_for_history(history: list[int]) -> int:
    diff_lists = [history]
    while True:
        next_list = get_diffs(diff_lists[-1])
        diff_lists.append(next_list)
        if all(map(is_zero, next_list)):
            break

    predicted_value = 0
    for diff_list in reversed(diff_lists):
        predicted_value = diff_list[0] - predicted_value

    return predicted_value


def read_input() -> list[list[int]]:
    with open("input.txt") as f:
        return [list(map(int, line.split())) for line in f]


def part_1():
    histories = read_input()
    next_values = list(map(predict_next_value_for_history, histories))
    return sum(next_values)


def part_2():
    histories = read_input()
    previous_values = list(map(predict_previous_value_for_history, histories))
    return sum(previous_values)


def sandbox():
    histories = [
        [0, 3, 6, 9, 12, 15],
        [1, 3, 6, 10, 15, 21],
        [10, 13, 16, 21, 30, 45],
    ]

    next_values = list(map(predict_next_value_for_history, histories))
    print(next_values)
    print(sum(next_values))

    previous_values = list(map(predict_previous_value_for_history, histories))
    print(previous_values)
    print(sum(previous_values))


if __name__ == "__main__":
    # sandbox()
    print("Part 1:", part_1())
    print("Part 2:", part_2())
