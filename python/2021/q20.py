import aocd


def parse_input(input):
    algorithm = ""
    a_part, i_part = input.split("\n\n")
    for line in a_part.splitlines():
        algorithm += line

    lit_pixels = set()
    for r, line in enumerate(i_part.splitlines()):
        for c, char in enumerate(line):
            if char == "#":
                lit_pixels.add((r, c))

    return algorithm, Image(lit_pixels)


class Image:
    lit_pixels: set
    min_row: int
    max_row: int
    min_col: int
    max_col: int
    outside_is_lit = False

    def __init__(self, lit_pixels):
        self.lit_pixels = lit_pixels
        self.update_extents()

    def update_extents(self):
        self.min_row = min(x[0] for x in self.lit_pixels)
        self.max_row = max(x[0] for x in self.lit_pixels)
        self.min_col = min(x[1] for x in self.lit_pixels)
        self.max_col = max(x[1] for x in self.lit_pixels)

    def is_lit(self, r, c):
        inside = (self.min_col <= c <= self.max_col) and (self.min_row <= r <= self.max_row)
        if inside:
            return (r, c) in self.lit_pixels
        else:
            return self.outside_is_lit

    def get_key(self, r, c):
        key = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                key <<= 1
                if self.is_lit(r + dr, c + dc):
                    key += 1
        return key

    def __str__(self):
        result = ""
        for row in range(self.min_row, self.max_row + 1):
            for col in range(self.min_col, self.max_col + 1):
                result += "#" if self.is_lit(row, col) else "."
            result += "\n"
        return result

    def enhance(self, algorithm, enlarge_by=1):
        new_pixels = set()
        for row in range(self.min_row - 1, self.max_row + 2):
            for col in range(self.min_col - 1, self.max_col + 2):
                key = self.get_key(row, col)
                if algorithm[key] == "#":
                    new_pixels.add((row, col))
        self.lit_pixels = new_pixels
        self.update_extents()
        self.outside_is_lit = algorithm[511 * self.outside_is_lit] == "#"

    def num_lit_bits(self):
        return len(self.lit_pixels)


def test():
    input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
    algorithm, image = parse_input(input)
    assert len(algorithm) == 512
    assert image.num_lit_bits() == 10
    assert image.get_key(2, 2) == 34

    [image.enhance(algorithm) for _ in range(2)]
    assert image.num_lit_bits() == 35, image.num_lit_bits()

    [image.enhance(algorithm) for _ in range(48)]
    assert image.num_lit_bits() == 3351, image.num_lit_bits()


def part_one(input):
    algorithm, image = parse_input(input)
    assert len(algorithm) == 512
    [image.enhance(algorithm) for _ in range(2)]
    result = image.num_lit_bits()
    assert result == 5306, result
    return result


def part_two(input):
    algorithm, image = parse_input(input)
    [image.enhance(algorithm) for _ in range(50)]
    result = image.num_lit_bits()
    return result


if __name__ == "__main__":
    test()
    input = aocd.get_data(day=20, year=2021)
    print(part_one(input))
    # print(part_two(input))
#
