import utils
from typing import List, Tuple
import aocd
from collections import defaultdict


def model_a_day(fish_timers):
    result = []
    new_fish_count = 0
    for timer in fish_timers:
        if timer == 0:
            new_timer = 6
            new_fish_count += 1
        else:
            new_timer = timer - 1
        result.append(new_timer)

    return result + [8] * new_fish_count


def part_one(data: List[int]) -> int:
    num_days = 80
    fish = data.copy()
    for day in range(num_days):
        fish = model_a_day(fish)
    return len(fish)


def model_a_day_2(fish_timers):
    # use dicts to keep a tally
    result = defaultdict(int)
    for k, v in fish_timers.items():
        if k == 0:
            result[6] += v
            result[8] += v
        else:
            result[k - 1] += v
    return result


def part_two(data: List[int]) -> int:
    num_days = 256
    fish_timers = defaultdict(int)
    for initial_timer in data:
        fish_timers[initial_timer] += 1

    for day in range(num_days):
        fish_timers = model_a_day_2(fish_timers)
        print(day, fish_timers)

    return sum(fish_timers.values())


def test():
    fish_timers = [2, 3, 2, 0, 1]
    result = model_a_day(fish_timers)
    assert result == [1, 2, 1, 6, 0, 8], result

    fish_timers_2 = {2: 2, 3: 1, 0: 1, 1: 1}
    result_2 = model_a_day_2(fish_timers_2)
    assert result_2 == {1: 2, 2: 1, 6: 1, 0: 1, 8: 1}, result_2
    result_3 = model_a_day_2(result_2)
    assert result_3 == {0: 2, 1: 1, 5: 1, 6: 1, 8: 1, 7: 1}, result_3


if __name__ == "__main__":
    test()
    data = [int(i) for i in aocd.get_data(day=6, year=2021).split(",")]
    print(part_one(data))
    print(part_two(data))
