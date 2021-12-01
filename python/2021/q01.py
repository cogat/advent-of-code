import utils
from typing import List
import aocd


def part_one(numbers: List[int]) -> int:
    """
    Find how many numbers are greater than the previous
    """
    greater_count = 0
    last_number = numbers[0]
    for n in numbers[1:]:
        if n > last_number:
            greater_count += 1
        last_number = n

    return greater_count


def part_two(numbers: List[int]) -> int:
    last_sum = None
    greater_count = 0
    for i in range(len(numbers) - 2):
        s = sum(numbers[i : i + 3])
        if last_sum and s > last_sum:
            greater_count += 1
        last_sum = s
    return greater_count


if __name__ == "__main__":
    numbers = utils.int_numbers(aocd.get_data(day=1, year=2021))
    print(part_one(numbers))
    print(part_two(numbers))
