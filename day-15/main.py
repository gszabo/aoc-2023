from pathlib import Path

def my_hash(s: str):
    current = 0

    for ch in s:
        current += ord(ch)
        current *= 17
        current %= 256

    return current


def part_1():
    input_line = Path("input.txt").read_text().strip()
    input_sequence = input_line.split(",")

    sum = 0

    for part in input_sequence:
        sum += my_hash(part)

    return sum


def part_2():
    input_line = Path("input.txt").read_text().strip()
    input_sequence = input_line.split(",")

    boxes = [{} for _ in range(256)]

    for part in input_sequence:
        if "=" in part:
            lens_label, focal_length = part.split("=")
            focal_length = int(focal_length)
            box_number = my_hash(lens_label)
            boxes[box_number][lens_label] = focal_length
        else:
            lens_label = part[:-1]
            box_number = my_hash(lens_label)
            boxes[box_number].pop(lens_label, None)

    sum = 0

    for i, box in enumerate(boxes):
        for j, (_, focal_length) in enumerate(box.items()):
            sum += (i + 1) * (j + 1) * focal_length

    return sum




def sandbox():
    print(my_hash("cm-"))


if __name__ == "__main__":
    # sandbox()
    print("Part 1:", part_1())
    print("Part 2:", part_2())
