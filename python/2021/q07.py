import aocd


COORD_REGEX = r"(\d+),(\d+) -> (\d+),(\d+)"


def part_one(data):
    return min(sum([abs(d - i) for d in data]) for i in range(min(data), max(data)))


# precalc triangle numbers
triangle_numbers = []
for i in range(10000):
    triangle_numbers.append(sum(range(i + 1)))


def part_two(data):
    return min(
        sum([triangle_numbers[abs(d - i)] for d in data]) for i in range(min(data), max(data))
    )


if __name__ == "__main__":
    data = [int(i) for i in aocd.get_data(day=7, year=2021).split(",")]
    print(part_one(data))
    print(part_two(data))
