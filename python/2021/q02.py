import utils
from typing import List, Tuple
import aocd

command_map = {"forward": (0, 1), "down": (1, 1), "up": (1, -1)}


def part_one(data: List[Tuple[str, int]]) -> int:
    """
    Find how many numbers are greater than the previous
    """
    position = [0, 0]  # horizontal, depth
    for direction, amount in data:
        index, mult = command_map[direction]
        position[index] += mult * amount

    return position[0] * position[1]


def part_two(data: List[Tuple[str, int]]) -> int:
    """
    Find how many numbers are greater than the previous
    """
    position = [0, 0, 0]  # horizontal, depth, aim
    for direction, amount in data:
        # print(direction)
        if direction == "down":
            position[2] += amount
        elif direction == "up":
            position[2] -= amount
        elif direction == "forward":
            position[0] += amount
            position[1] += position[2] * amount

    return position[0] * position[1]


if __name__ == "__main__":
    data = utils.parse_lines(aocd.get_data(day=2, year=2021), separator=" ", types=(str, int))
    print(part_one(data))
    print(part_two(data))
