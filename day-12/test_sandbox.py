from itertools import groupby


def calc_groups(record: str) -> list[int]:
    return [len(list(group)) for char, group in groupby(record) if char == "#"]


def calc_possible_groups(record: str) -> list[int]:
    record = record.replace("?", "#")
    return [len(list(group)) for char, group in groupby(record) if char == "#"]


def test_calc_groups():
    assert calc_groups("") == []
    assert calc_groups(".") == []
    assert calc_groups("..") == []
    assert calc_groups("#") == [1]
    assert calc_groups("##") == [2]
    assert calc_groups("#.##") == [1, 2]
    assert calc_groups("#?##") == [1, 2]


def test_vmi():
    record = ".??..??...?##."
    desired_groups = [1, 1, 3]

    # current_groups = calc_groups(record)
    # possible_groups = calc_possible_groups(record)

    def inner_count(text: str) -> int:
        # print(text)
        groups = calc_groups(text)
        if "?" not in text:
            return 1 if groups == desired_groups else 0

        # for i in range(min(len(groups), len(desired_groups))):
        #     if groups[i] > desired_groups[i]:
        #         return 0

        return inner_count(text.replace("?", "#", 1)) + inner_count(text.replace("?", ".", 1))

    print(inner_count(record))


    assert False
