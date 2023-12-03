from collections import defaultdict
from operator import itemgetter


def parse_input():
    with open("input.txt") as f:
        lines = f.readlines()
        games = []
        for line in lines:
            line = line.strip()
            before_colon, after_colon = line.split(":")

            game = {}
            game["id"] = int(before_colon.split(" ")[1])
            game["reveals"] = []

            for reveal in after_colon.split(";"):
                reveal = reveal.strip()
                reveal_dict = defaultdict(int)
                for cube in reveal.split(","):
                    cube = cube.strip()
                    count, color = cube.split(" ")
                    reveal_dict[color] = int(count)

                game["reveals"].append(reveal_dict)
            games.append(game)
        return games


def part_1():
    max_red = 12
    max_green = 13
    max_blue = 14

    games = parse_input()

    sum = 0

    for game in games:
        if all(
            [
                reveal["red"] <= max_red
                and reveal["green"] <= max_green
                and reveal["blue"] <= max_blue
                for reveal in game["reveals"]
            ]
        ):
            sum += game["id"]

    return sum


def part_2():
    games = parse_input()

    sum = 0

    for game in games:
        min_red_required = max(map(itemgetter("red"), game["reveals"]))
        min_green_required = max(map(itemgetter("green"), game["reveals"]))
        min_blue_required = max(map(itemgetter("blue"), game["reveals"]))

        power = min_red_required * min_green_required * min_blue_required

        sum += power

    return sum


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
