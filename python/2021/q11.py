import aocd
from collections import deque


class Grid:
    def __init__(self, input_lines):
        self.values = [[int(c) for c in line.strip()] for line in input_lines]
        self.flashers = deque()

    def __str__(self):
        return "\n".join(["".join([str(i) for i in line]) for line in self.values])

    def coord_at(self, r, c):
        return self.values[r][c]

    @property
    def num_columns(self):
        return len(self.values[0])

    @property
    def num_rows(self):
        return len(self.values)

    @property
    def size(self):
        return self.num_columns * self.num_rows

    def neighbours(self, r, c):
        for rx, cx in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= rx < self.num_rows and 0 <= cx < self.num_columns:
                yield (rx, cx)

    def diagonal_neighbours(self, r, c):
        for rx, cx in [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
            (r - 1, c - 1),
            (r - 1, c + 1),
            (r + 1, c - 1),
            (r + 1, c + 1),
        ]:
            if 0 <= rx < self.num_rows and 0 <= cx < self.num_columns:
                yield (rx, cx)

    def boost_energy(self, r, c):
        self.values[r][c] += 1
        if self.values[r][c] > 9:
            self.flashers.append((r, c))

    def simulate_flashes(self) -> int:
        for r in range(self.num_rows):
            for c in range(self.num_columns):
                self.boost_energy(r, c)

        already_flashed = set()
        while self.flashers:
            r, c = self.flashers.popleft()
            if (r, c) not in already_flashed:
                already_flashed.add((r, c))
                for neighbour in self.diagonal_neighbours(r, c):
                    self.boost_energy(*neighbour)

        for r, c in already_flashed:
            self.values[r][c] = 0

        return len(already_flashed)


def part_one(input_lines):
    grid = Grid(input_lines)
    total = 0
    for r in range(100):
        total += grid.simulate_flashes()
    return total


def part_two(input_lines):
    grid = Grid(input_lines)
    step_count = 1
    while grid.simulate_flashes() != grid.size:
        step_count += 1
    return step_count


def test():
    input = """11111
19991
19191
19991
11111"""
    grid = Grid(input.splitlines())
    flash_count = grid.simulate_flashes()
    grid_values = str(grid)
    assert flash_count == 9
    assert (
        grid_values
        == """34543
40004
50005
40004
34543"""
    ), grid_values


if __name__ == "__main__":
    test()
    lines = aocd.get_data(day=11, year=2021).splitlines()
    print(part_one(lines))
    print(part_two(lines))
