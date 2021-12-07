import utils
from typing import List, Optional
import aocd
from dataclasses import dataclass, field
import re
from collections import defaultdict


COORD_REGEX = r"(\d+),(\d+) -> (\d+),(\d+)"


class Grid:
    def __init__(self):
        self.grid = defaultdict(int)

    def increment(self, *coord):
        self.grid[coord] += 1

    def num_points_gte(self, n):
        return sum(i >= n for i in self.grid.values())


def fullrange(i1, i2):
    if i2 < i1:
        return range(i2, i1 + 1)
    else:
        return range(i1, i2 + 1)


def part_one(data):
    grid = Grid()

    for line in data:
        x1, y1, x2, y2 = [int(m) for m in re.match(COORD_REGEX, line).groups()]
        if x1 == x2:
            for y in fullrange(y1, y2):
                grid.increment(x1, y)
        elif y1 == y2:
            for x in fullrange(x1, x2):
                grid.increment(x, y1)
        else:
            continue

    return grid.num_points_gte(2)


def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def coordrange(x1, y1, x2, y2):
    """
    Return coord pairs of x, y along the line x1,y1 to x2,y2. The line may lie along any
    angle that is a multiple of 45 degrees
    """
    x = x1
    y = y1
    xinc = sign(x2 - x1)
    yinc = sign(y2 - y1)
    while x != x2 or y != y2:
        yield x, y
        # move x, y closer to x2, y2
        x += xinc
        y += yinc
    yield x, y


def part_two(data):
    grid = Grid()

    for line in data:
        c = [int(m) for m in re.match(COORD_REGEX, line).groups()]
        for coord in coordrange(*c):
            grid.increment(*coord)

    return grid.num_points_gte(2)


def test():
    data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".splitlines()
    assert part_one(data) == 5, part_one(data)
    assert part_two(data) == 12, part_two(data)


if __name__ == "__main__":
    test()
    data = aocd.get_data(day=5, year=2021).splitlines()
    print(part_one(data))
    print(part_two(data))
