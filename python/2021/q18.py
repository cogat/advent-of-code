import aocd
import math


class SFN:  # snailfishnumber
    children: list

    def __init__(self, children):
        assert len(children) == 2
        r = []
        for child in children:
            if isinstance(child, int):
                r.append(child)
            else:
                r.append(SFN(children=child))

        self.children = r

    def as_list(self):
        r = []
        for child in self.children:
            if isinstance(child, int):
                r.append(child)
            else:
                r.append(child.as_list())
        return r

    def __add__(self, other: "SFN"):
        return SFN((self.as_list(), other.as_list())).reduce()

    def __str__(self):
        return str(self.children)

    def __repr__(self):
        return str(self.children)

    def digit_paths(self, path=[]):
        # breadth-first recursion
        for i, c in enumerate(self.children):
            if isinstance(c, int):
                yield c, path + [i]
            else:
                yield from c.digit_paths(path + [i])

    def get_value_at_path(self, path):
        v = self
        for p in path:
            v = v.children[p]
        return v

    def set_value_at_path(self, path, value):
        v = self
        for p in path[:-1]:
            v = v.children[p]
        v.children[path[-1]] = value

    def _reduce_step(self):
        digit_paths = list(self.digit_paths())
        for i, digit_path in enumerate(digit_paths):  # look for any explodes
            digit, path = digit_path
            if len(path) == 5:  # 5 = root + 4 nests
                assert len(digit_paths[i + 1][1]) == 5, digit_paths[i + 1][1]
                if i > 0:
                    left = digit
                    path_to_prev_digit = digit_paths[i - 1][1]
                    self.set_value_at_path(
                        path_to_prev_digit, self.get_value_at_path(path_to_prev_digit) + left
                    )
                if i + 2 < len(digit_paths):
                    right = digit_paths[i + 1][0]
                    path_to_next_digit = digit_paths[i + 2][1]
                    self.set_value_at_path(
                        path_to_next_digit, self.get_value_at_path(path_to_next_digit) + right
                    )
                # replace this tuple with 0 then exit
                self.set_value_at_path(path[:-1], 0)
                return self

        for i, digit_path in enumerate(digit_paths):  # look for any splits
            digit, path = digit_path
            if digit >= 10:  # split
                self.set_value_at_path(
                    path,
                    SFN([digit // 2, int(math.ceil(digit / 2))]),
                )
                return self
        return None

    def reduce(self):
        while True:
            next_step = self._reduce_step()
            if next_step is None:
                return self

    def magnitude(self):
        mag = 0
        for i, c in enumerate(self.children):
            if isinstance(c, int):
                if i == 0:
                    mag += 3 * c
                else:
                    mag += 2 * c
            else:
                if i == 0:
                    mag += 3 * c.magnitude()
                else:
                    mag += 2 * c.magnitude()
        return mag


def test():
    t = [[[[[9, 8], 1], 2], 3], 4]
    assert SFN(t).as_list() == t

    add = SFN([1, 2]) + SFN([[3, 4], 5])
    assert add.as_list() == [[1, 2], [[3, 4], 5]], add

    number = SFN([[3, [2, [1, [7, 9]]]], [6, [5, [4, [3, 2]]]]])
    digit_paths = list(number.digit_paths())
    assert digit_paths == [
        (3, [0, 0]),
        (2, [0, 1, 0]),
        (1, [0, 1, 1, 0]),
        (7, [0, 1, 1, 1, 0]),
        (9, [0, 1, 1, 1, 1]),
        (6, [1, 0]),
        (5, [1, 1, 0]),
        (4, [1, 1, 1, 0]),
        (3, [1, 1, 1, 1, 0]),
        (2, [1, 1, 1, 1, 1]),
    ], digit_paths
    number.set_value_at_path([0, 1, 1, 1, 1], 3)
    assert number.get_value_at_path([0, 1, 1, 1, 1]) == 3

    reduced_once = number._reduce_step()
    assert reduced_once.as_list() == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], reduced_once

    for number, expected in (
        ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
        ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
        ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
        ([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]),
    ):
        result = SFN(number).reduce()
        assert result.as_list() == expected, result

    for number, expected in (
        ([9, 1], 29),
        ([1, 9], 21),
        ([[1, 2], [[3, 4], 5]], 143),
        ([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]], 1384),
        ([[[[1, 1], [2, 2]], [3, 3]], [4, 4]], 445),
        ([[[[3, 0], [5, 3]], [4, 4]], [5, 5]], 791),
        ([[[[5, 0], [7, 4]], [5, 5]], [6, 6]], 1137),
        ([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]], 3488),
    ):
        magnitude = SFN(number).magnitude()
        assert magnitude == expected, magnitude

    sfn1 = SFN([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
    sfn2 = SFN([1, 1])
    expected = [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    result = sfn1 + sfn2
    assert result.as_list() == expected, result

    sfn1 = SFN([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]])
    sfn2 = SFN([7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]])
    expected = [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]
    result = sfn1 + sfn2
    assert result.as_list() == expected, result

    input = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
    result = sum_input(input)
    assert result.as_list() == [
        [[[8, 7], [7, 7]], [[8, 6], [7, 7]]],
        [[[0, 7], [6, 6]], [8, 7]],
    ], result

    input = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
    result = sum_input(input)
    assert result.as_list() == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]], result

    input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""
    result = sum_input(input)
    assert result.as_list() == [
        [[[6, 6], [7, 6]], [[7, 7], [7, 0]]],
        [[[7, 7], [7, 7]], [[7, 8], [9, 9]]],
    ], result
    assert result.magnitude() == 4140, result.magnitude()


def sum_input(input):
    tally = None
    for line in input.splitlines():
        sfn = SFN(eval(line))
        if tally is None:
            tally = sfn
        else:
            tally += sfn
    return tally


def part_one(input):
    return sum_input(input).magnitude()


def part_two(input):
    max_mag = 0
    sfns = [SFN(eval(line)) for line in input.splitlines()]
    for sfn1 in sfns:
        for sfn2 in sfns:
            max_mag = max(max_mag, (sfn1 + sfn2).magnitude())
    return max_mag


if __name__ == "__main__":
    test()
    input = aocd.get_data(day=18, year=2021)
    print("Part One: ", part_one(input))
    print("Part Two: ", part_two(input))
