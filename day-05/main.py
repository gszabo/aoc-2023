from functools import reduce, partial
from itertools import islice
from typing import Optional

from input import (
    SEEDS,
    SEED_TO_SOIL,
    SOIL_TO_FERTILIZER,
    FERTILIZER_TO_WATER,
    WATER_TO_LIGHT,
    LIGHT_TO_TEMPERATURE,
    TEMPERATURE_TO_HUMIDITY,
    HUMIDITY_TO_LOCATION,
)


class ObscureMapping:
    _config: list[tuple[int, int, int]]

    def __init__(self, config):
        self._config = config

    def __call__(self, key: int) -> int:
        for dest_range_start, source_range_start, range_len in self._config:
            if source_range_start <= key < source_range_start + range_len:
                return dest_range_start + (key - source_range_start)
        return key

    def inverse(self, key: int) -> int:
        for dest_range_start, source_range_start, range_len in self._config:
            if dest_range_start <= key < dest_range_start + range_len:
                return source_range_start + (key - dest_range_start)
        return key


def part_1():
    mappings = [
        ObscureMapping(SEED_TO_SOIL),
        ObscureMapping(SOIL_TO_FERTILIZER),
        ObscureMapping(FERTILIZER_TO_WATER),
        ObscureMapping(WATER_TO_LIGHT),
        ObscureMapping(LIGHT_TO_TEMPERATURE),
        ObscureMapping(TEMPERATURE_TO_HUMIDITY),
        ObscureMapping(HUMIDITY_TO_LOCATION),
    ]

    combined_mapper_fn = partial(reduce, lambda x, f: f(x), mappings)

    return min(map(combined_mapper_fn, SEEDS))


def part_2():
    # iterating over the real seeds is too slow, it's just too many numbers (even just printing them is too slow)
    # and the task is to find the lowest location that corresponds to any seed
    # so I invert the function chain and go from location to seed value.
    # My plan is to find the lowest location by first trying 0, 1, 2, 4, 8, 16, 32, 64, 128, 256, ...
    # as location values, and checking if any of them (after applying the inverse chain) falls into
    # any of the seed ranges. If 2^N does, then I know that the lowest location is between 2^(N-1) and 2^N.
    # Binary search can then be applied to the 2^(N-1) to 2^N range to find the lowest location.

    inverse_mappings = [
        ObscureMapping(HUMIDITY_TO_LOCATION).inverse,
        ObscureMapping(TEMPERATURE_TO_HUMIDITY).inverse,
        ObscureMapping(LIGHT_TO_TEMPERATURE).inverse,
        ObscureMapping(WATER_TO_LIGHT).inverse,
        ObscureMapping(FERTILIZER_TO_WATER).inverse,
        ObscureMapping(SOIL_TO_FERTILIZER).inverse,
        ObscureMapping(SEED_TO_SOIL).inverse,
    ]

    combined_inverse_mapper_fn = partial(reduce, lambda x, f: f(x), inverse_mappings)

    seed_ranges = list(zip(SEEDS[::2], SEEDS[1::2]))

    def is_valid_seed(seed: int) -> bool:
        return any(start <= seed < start + length for start, length in seed_ranges)

    i = 0
    while True:
        location = 2**i
        seed = combined_inverse_mapper_fn(location)
        is_valid = is_valid_seed(seed)
        if is_valid:
            # binary search
            lower_bound = 2 ** (i - 1)
            upper_bound = 2 ** i
            while lower_bound < upper_bound:
                mid = (lower_bound + upper_bound) // 2
                if is_valid_seed(combined_inverse_mapper_fn(mid)):
                    upper_bound = mid
                else:
                    lower_bound = mid + 1

            return lower_bound
        i += 1


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
