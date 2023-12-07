from itertools import groupby


HAND_ORDER_BY_GROUPS = {
    (5,): 7,  # five of a kind
    (4, 1): 6,  # four of a kind
    (3, 2): 5,  # full house
    (3, 1, 1): 4,  # three of a kind
    (2, 2, 1): 3,  # two pairs
    (2, 1, 1, 1): 2,  # one pair
    (1, 1, 1, 1, 1): 1,  # high card
}

CARD_ORDER = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CARD_ORDER_WITH_JOKER = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


class Hand:
    _cards: str
    _groups: tuple

    def __init__(self, cards: str):
        self._cards = cards
        self._groups = tuple(
            sorted(
                [len(list(group)) for _, group in groupby(sorted(cards))],
                reverse=True,
            )
        )

    def __repr__(self):
        return self._cards

    def __lt__(self, other):
        self_group = HAND_ORDER_BY_GROUPS[self._groups]
        other_group = HAND_ORDER_BY_GROUPS[other._groups]

        if self_group != other_group:
            return self_group < other_group

        for self_card, other_card in zip(self._cards, other._cards):
            if CARD_ORDER[self_card] != CARD_ORDER[other_card]:
                return CARD_ORDER[self_card] < CARD_ORDER[other_card]

        return False

    def __eq__(self, other):
        return self._cards == other._cards


class JokerHand:
    _cards: str
    _groups: tuple

    def __init__(self, cards: str):
        self._cards = cards

        joker_count = cards.count("J")
        if joker_count == 5:
            self._groups = (5,)
        else:
            cards_without_joker = cards.replace("J", "")
            groups = list(
                sorted(
                    [len(list(group)) for _, group in groupby(sorted(cards_without_joker))],
                    reverse=True,
                )
            )
            groups[0] += joker_count
            self._groups = tuple(groups)


    def __repr__(self):
        return self._cards

    def __lt__(self, other):
        self_group = HAND_ORDER_BY_GROUPS[self._groups]
        other_group = HAND_ORDER_BY_GROUPS[other._groups]

        if self_group != other_group:
            return self_group < other_group

        for self_card, other_card in zip(self._cards, other._cards):
            if CARD_ORDER_WITH_JOKER[self_card] != CARD_ORDER_WITH_JOKER[other_card]:
                return CARD_ORDER_WITH_JOKER[self_card] < CARD_ORDER_WITH_JOKER[other_card]

        return False

    def __eq__(self, other):
        return self._cards == other._cards


def parse_input():
    with open("input.txt", "r") as f:
        return [((parts := line.split())[0], int(parts[1])) for line in f]


def part_1():
    data = [(Hand(cards), bid) for cards, bid in parse_input()]
    sorted_data = sorted(data, key=lambda x: x[0])
    return sum([(index + 1) * bid for index, (hand, bid) in enumerate(sorted_data)])


def part_2():
    data = [(JokerHand(cards), bid) for cards, bid in parse_input()]
    sorted_data = sorted(data, key=lambda x: x[0])
    return sum([(index + 1) * bid for index, (hand, bid) in enumerate(sorted_data)])


def debug():
    print("########### DEBUG ############")
    data = [(Hand(cards), JokerHand(cards)) for cards, bid in parse_input()]
    for hand, joker_hand in data:
        if hand._groups != joker_hand._groups:
            print(f"{hand} {hand._groups} -> {joker_hand._groups}")


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
    # debug()
