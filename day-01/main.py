from pathlib import Path


DIGITS_SPELLED_OUT_WITH_LETTERS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

DIGITS = list("123456789")


EVERY_DIGIT = DIGITS + DIGITS_SPELLED_OUT_WITH_LETTERS

def convert_digit_to_value(digit: str) -> int:
    if digit.isdigit():
        return int(digit)
    else:
        return DIGITS_SPELLED_OUT_WITH_LETTERS.index(digit) + 1


def read_input():
    # read in every line of input.txt
    path = Path(__file__).parent / "input.txt"
    lines = path.read_text().splitlines()

    return lines


def part_1():
    lines = read_input()

    sum = 0

    for line in lines:
        digits = list(filter(str.isdigit, line))
        first_digit = digits[0]
        last_digit = digits[-1]
        number = int(f"{first_digit}{last_digit}")
        sum += number

    return sum


def part_2():
    lines = read_input()

    sum = 0

    for line in lines:
        digits_in_line = list(filter(line.__contains__, EVERY_DIGIT))

        first_digit = min(digits_in_line, key=line.find)
        last_digit = max(digits_in_line, key=line.rfind)

        first_digit_value = convert_digit_to_value(first_digit)
        last_digit_value = convert_digit_to_value(last_digit)

        number = first_digit_value * 10 + last_digit_value

        sum += number

    return sum


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
