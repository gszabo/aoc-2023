def parse_input():
    # read input txt
    # each line looks line:
    # Card (one or more whitespace) <id>: <list of winning numbers separated by one or more space> | <list of numbers separated by one or more space>
    # For example: Card   4: 22 99 16 18 81  3 62 43  2 42 |  8 55 39 83 29 10 87 27 25 70 19 30 80 12  1 41 85 14 34 82 90 76  5 89 15
    # return a list of dicts
    # expected output for the example above:
    # [
    #   {
    #     "id": "4",
    #     "winning_numbers": ["22", "99", "16", "18", "81", "3", "62", "43", "2", "42"],
    #     "numbers": ["8", "55", "39", "83", "29", "10", "87", "27", "25", "70", "19", "30", "80", "12", "1", "41", "85", "14", "34", "82", "90", "76", "5", "89", "15"]
    #   }
    # ]
    with open("input.txt") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    cards = []
    for line in lines:
        card = {}
        card["id"] = line.split(":")[0].split()[1]
        card["winning_numbers"] = list(
            map(int, line.split("|")[0].split(":")[1].split())
        )
        card["numbers"] = list(map(int, line.split("|")[1].split()))
        cards.append(card)
    return cards


def part_1():
    cards = parse_input()

    sum_point = 0

    for card in cards:
        good_numbers = [
            number for number in card["numbers"] if number in card["winning_numbers"]
        ]
        if len(good_numbers) > 0:
            sum_point += 2 ** (len(good_numbers) - 1)

    return sum_point


def part_2():
    cards = parse_input()

    wins = list(
        map(
            lambda card: len(
                [
                    number
                    for number in card["numbers"]
                    if number in card["winning_numbers"]
                ]
            ),
            cards,
        )
    )

    amount_by_cards = [1 for _ in range(len(cards))]

    for index, n in enumerate(wins):
        for j in range(index + 1, min(index + n + 1, len(cards))):
            amount_by_cards[j] += amount_by_cards[index]

    return sum(amount_by_cards)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
