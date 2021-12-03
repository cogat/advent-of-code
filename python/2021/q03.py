import utils
from typing import List
import aocd


def part_one(data: List[str]) -> int:
    """
    Construct a binary number from the most common bits in the input
    """
    length = len(data[0])
    tally = [0] * length
    for d in data:
        for i in range(length):
            tally[i] += 1 if d[i] == "1" else -1

    gamma_digits = "".join(["1" if x > 0 else "0" for x in tally])
    epsilon_digits = "".join(["0" if x > 0 else "1" for x in tally])
    gamma = int(gamma_digits, 2)
    epsilon = int(epsilon_digits, 2)
    return gamma * epsilon


def _filter_by_digit(data, position, digit):
    return list(filter(lambda row: row[position] == digit, data))


def _most_common_digit_at_position(data, position) -> str:
    result = 0
    for row in data:
        result += 1 if row[position] == "1" else -1
    return "1" if result >= 0 else "0"


def _least_common_digit_at_position(data, position) -> str:
    return "1" if _most_common_digit_at_position(data, position) == "0" else "0"


def part_two(data: List[int]) -> int:
    length = len(data[0])
    data2 = data.copy()

    for d in range(length):
        mcd = _most_common_digit_at_position(data, d)
        data = _filter_by_digit(data, d, mcd)
        if len(data) == 1:
            break

    for d in range(length):
        lcd = _least_common_digit_at_position(data2, d)
        data2 = _filter_by_digit(data2, d, lcd)
        if len(data2) == 1:
            break

    o2 = int("".join(data), 2)
    co2 = int("".join(data2), 2)

    return o2 * co2


if __name__ == "__main__":
    data = utils.parse_lines(aocd.get_data(day=3, year=2021), str)
    print(part_one(data))
    print(part_two(data))
