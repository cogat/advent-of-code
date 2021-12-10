import aocd
from collections import defaultdict
from typing import Tuple


def check_line(line) -> Tuple[int, list]:
    # return the failure score or the incomplete stack
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
            continue
        try:
            if char == ")":
                assert stack.pop() == "(", (3, [])
            if char == "]":
                assert stack.pop() == "[", (57, [])
            if char == "}":
                assert stack.pop() == "{", (1197, [])
            if char == ">":
                assert stack.pop() == "<", (25137, [])
        except AssertionError as e:
            return e.args[0]
    return 0, stack


completion_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
score_map = {")": 1, "]": 2, "}": 3, ">": 4}


def get_completion_score(s):  # s should be close brackets
    char_scores = [score_map[c] for c in s]
    total = 0
    for sc in char_scores:
        total *= 5
        total += sc
    return total


def part_one(lines):
    return sum([check_line(line)[0] for line in lines])


def part_two(lines):
    line_totals = []
    for line in lines:
        _, incomplete = check_line(line)
        if incomplete:
            completion = [completion_map[c] for c in reversed(incomplete)]
            line_totals.append(get_completion_score(completion))
    return sorted(line_totals)[len(line_totals) // 2]


def test():
    a, b = check_line("{([(<{}[<>[]}>{[]{[(<()>")
    assert a == 1197, a
    assert b == [], b

    c = get_completion_score("}}]])})]")
    assert c == 288957, c


if __name__ == "__main__":
    test()
    lines = aocd.get_data(day=10, year=2021).splitlines()
    print(part_one(lines))
    print(part_two(lines))
