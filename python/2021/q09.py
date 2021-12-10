import aocd
from collections import defaultdict


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
                return
        return coord  # coord is not greater than or equal to any of its neigbours

    def inside(self, r, c) -> bool:
        if 0 <= r < self.num_rows and 0 <= c < self.num_columns:
            return self.coord_at(r, c) < 9
        return False

    def _map_basin(self, found_already: set, r, c) -> set:
        if not self.inside(r, c):
            return found_already

        found_already.add((r, c))
        for pair in self.neighbours(r, c):
            if pair not in found_already:
                found_already = self._map_basin(found_already, *pair)

        return found_already

    def basin_size(self, r, c) -> int:
        basin_coords = self._map_basin(set(), r, c)
        return len(basin_coords)


def part_one(input_lines):
    grid = Grid(input_lines)
    risk = 0
    for r in range(grid.num_rows):
        for c in range(grid.num_columns):
            n = grid.coord_is_lower_than_neighbours(r, c)
            if n is not None:
                risk += n + 1

    return risk


def part_two(input_lines):
    grid = Grid(input_lines)
    basin_sizes = []
    for r in range(grid.num_rows):
        for c in range(grid.num_columns):
            n = grid.coord_is_lower_than_neighbours(r, c)
            if n is not None:
                basin_sizes.append(grid.basin_size(r, c))

    sorted_sizes = sorted(basin_sizes)
    return sorted_sizes[-3] * sorted_sizes[-2] * sorted_sizes[-1]


def test():
    input = """2199943210
3987894921
9856789892
8767896781
9899965678"""
    answer = part_one(input.splitlines())
    assert answer == 17, answer


if __name__ == "__main__":
    test()
    lines = aocd.get_data(day=9, year=2021).splitlines()
    print(part_one(lines))
    print(part_two(lines))
