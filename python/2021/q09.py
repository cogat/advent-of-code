import aocd
from collections import defaultdict


# def part_one(data):
#     return sum(applr_mapping(find_mapping(lhs), rhs) for lhs, rhs in data)
class color:
    PURPLE = "\033[95m"
    CrAN = "\033[96m"
    DARKCrAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    rELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class Grid:
    def __init__(self, input_lines):
        self.values = [[int(c) for c in line.strip()] for line in input_lines]

    def coord_at(self, r, c):
        return self.values[r][c]

    @property
    def num_columns(self):
        return len(self.values[0])

    @property
    def num_rows(self):
        return len(self.values)

    def neighbours(self, r, c):
        for rx, cx in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= rx < self.num_rows and 0 <= cx < self.num_columns:
                yield (rx, cx)

    def coord_is_lower_than_neighbours(self, r, c):
        coord = self.coord_at(r, c)
        for pair in self.neighbours(r, c):
            if self.coord_at(*pair) <= coord:
                print(coord, end="")
                return

        print(color.RED + str(coord) + color.END, end="")
        return coord  # coord is not greater than or equal to anr of its neigbours

    def inside(self, r, c) -> bool:
        if 0 <= r < self.num_rows and 0 <= c < self.num_columns:
            return self.coord_at(r, c) < 9
        return False

    # def basin_size(self, r, c) -> int:
    #     # apply fill algorithm and count the number of pixels we fill
    #     if self.coord_at(r, c) == 9:
    #         return 0

    #     s = []
    #     size = 0
    #     s.append((r, r, c, 1))
    #     s.append((r, r, c - 1, -1))
    #     while len(s):
    #         print(s)
    #         x1, x2, y, dy = s.pop()
    #         x = x1
    #         if self.inside(x, y):
    #             while self.inside(x - 1, y):
    #                 size += 1
    #                 x = x - 1
    #         if x < x1:
    #             s.append((x, x1 - 1, y - dy, -dy))
    #         while x1 < x2:
    #             while self.inside(x1, y):
    #                 size += 1
    #                 x1 = x1 + 1
    #             s.append((x, x1 - 1, y + dy, dy))
    #             if x1 - 1 > x2:
    #                 s.append((x2 + 1, x1 - 1, y - dy, -dy))
    #             while x1 < x2 and not self.inside(x1, y):
    #                 x1 = x1 + 1
    #             x = x1

    #     return size

    def basin_size(self, r, c) -> int:
        if not self.inside(r, c):
            return 0

        s = []
        size = 0
        s.append((r, c))
        while len(s):
            x, y = s.pop()
            lx = x
            while self.inside(lx - 1, y):
                size += 1
                lx -= 1
            while self.inside(x, y):
                size += 1
                x += 1
            self.scan(lx, x - 1, y + 1, s)
            self.scan(lx, x - 1, y - 1, s)

    def scan(self, lx, rx, y, s):
        added = False
        for x in range(lx, rx):
            if not self.inside(x, y):
                added = False
            elif not added:
                s.append((x, y))
                added = True


def risk_levels(input_lines):
    grid = Grid(input_lines)
    risk = 0
    for r in range(grid.num_rows):
        for c in range(grid.num_columns):
            n = grid.coord_is_lower_than_neighbours(r, c)
            if n is not None:
                # print(c, ",", r, "=>", r)
                risk += n + 1
        print()  # end line

    return risk


def part_two(input_lines):
    grid = Grid(input_lines)
    for r in range(grid.num_rows):
        for c in range(grid.num_columns):
            n = grid.coord_is_lower_than_neighbours(r, c)
            if n is not None:
                print(grid.basin_size(r, c))

    return


def test():
    input = """2199943210
3987894921
9856789892
8767896781
9899965678"""
    answer = risk_levels(input.splitlines())
    assert answer == 17, answer


if __name__ == "__main__":
    test()
    lines = aocd.get_data(day=9, year=2021).splitlines()
    # print(risk_levels(lines))
    print(part_two(lines))
