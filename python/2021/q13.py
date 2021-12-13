import aocd
from collections import defaultdict
import re


class Grid:
    def __init__(self, input_lines):
        self.x_size = 0
        self.y_size = 0
        self.values = defaultdict(bool)
        for line in input_lines:
            x, y = [int(n) for n in line.strip().split(",")]
            self.x_size = max(self.x_size, x + 1)
            self.y_size = max(self.y_size, y + 1)
            self.values[(x, y)] = True

    def __str__(self):
        result = ""
        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.values[(x, y)]:
                    result += "#"
                else:
                    result += "."
            result += "\n"
        return result

    def fold_y(self, value):
        for y in range(value, self.y_size):
            for x in range(self.x_size):
                self.values[(x, value - (y - value))] |= self.values[(x, y)]

        self.y_size = value

    def fold_x(self, value):
        for x in range(value, self.x_size):
            for y in range(self.y_size):
                self.values[(value - (x - value), y)] |= self.values[(x, y)]

        self.x_size = value

    def apply_folds(self, folds, limit=None):
        for fold in folds[:limit]:
            dim, value = re.match(r"fold along (.)=(\d+)", fold).groups()
            if dim == "x":
                self.fold_x(int(value))
            elif dim == "y":
                self.fold_y(int(value))

    def num_dots(self):
        count = 0
        for x in range(self.x_size):
            for y in range(self.y_size):
                if self.values[(x, y)]:
                    count += 1
        return count


def part_one(coords, folds):
    grid = Grid(coords)
    grid.apply_folds(folds, limit=1)
    return grid.num_dots()


def part_two(coords, folds):
    grid = Grid(coords)
    grid.apply_folds(folds)
    return str(grid)


def test():
    input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
    coords, folds = get_coords_and_folds(input.splitlines())
    assert len(coords) == 18
    assert len(folds) == 2
    grid = Grid(coords)
    grid.apply_folds(folds)
    result = str(grid)
    assert (
        result
        == """#####
#...#
#...#
#...#
#####
.....
.....
"""
    ), result
    num_dots = grid.num_dots()
    assert num_dots == 16, num_dots


def get_coords_and_folds(lines):
    coords = []
    folds = []
    add_to_coords = True
    for line in lines:
        if not line:
            add_to_coords = False
            continue
        if add_to_coords:
            coords.append(line)
        else:
            folds.append(line)

    return coords, folds


if __name__ == "__main__":
    test()
    lines = aocd.get_data(day=13, year=2021).splitlines()
    coords, folds = get_coords_and_folds(lines)
    print(part_one(coords, folds))
    print(part_two(coords, folds))
