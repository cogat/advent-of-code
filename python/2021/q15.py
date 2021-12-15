from collections import defaultdict
from typing import Dict
import aocd
from astar import AStar


class RiskMazeSolver(AStar):

    """sample use of the astar algorithm. In this exemple we work on a maze made of ascii characters,
    and a 'node' is just a (x,y) tuple that represents a reachable position"""

    def __init__(self, lines):
        self.risks = [[int(c) for c in line] for line in lines.splitlines()]

    def __str__(self):
        result = ""
        for row in range(self.height):
            for col in range(self.width):
                result += str(self.risks[row][col])
            result += "\n"
        return result

    @property
    def width(self):
        return len(self.risks[0])

    @property
    def height(self):
        return len(self.risks)

    def heuristic_cost_estimate(self, n1, n2):
        """computes the 'direct' distance between two (x,y) tuples"""
        return 1  # I think setting this to 1 is equivalent to Dijkstra

    def distance_between(self, n1, n2):
        """return the risk increase of the destination"""
        return self.risks[n2[0]][n2[1]]

    def neighbors(self, node):
        x, y = node
        return [
            (nx, ny)
            for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
            if 0 <= nx < self.width and 0 <= ny < self.height
        ]

    def risk_sum(self, path):
        sum = 0
        for p in list(path)[1:]:
            sum += self.risks[p[0]][p[1]]
        return sum

    def expand_field(self, factor=5):
        new_risks = defaultdict(lambda: defaultdict(int))
        for row_inc in range(factor):
            for col_inc in range(factor):
                increase = row_inc + col_inc
                for row in range(self.height):
                    for col in range(self.width):
                        new_row = self.height * row_inc + row
                        new_col = self.width * col_inc + col
                        new_value = self.risks[row][col] + increase
                        if new_value > 9:
                            new_value -= 9
                        new_risks[new_row][new_col] = new_value
        self.risks = new_risks


def test():
    input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    gg = RiskMazeSolver(input)
    path = gg.astar((0, 0), (gg.width - 1, gg.height - 1))
    result = gg.risk_sum(path)
    assert result == 40, result

    input_2 = """19
23"""
    gg_2 = RiskMazeSolver(input_2)
    gg_2.expand_field(factor=2)
    assert (
        str(gg_2)
        == """1921
2334
2132
3445
"""
    ), str(gg_2)


def part_one(input):
    gg = RiskMazeSolver(input)
    path = gg.astar((0, 0), (gg.width - 1, gg.height - 1))
    result = gg.risk_sum(path)
    assert result == 604
    return result


def part_two(input):
    gg = RiskMazeSolver(input)
    gg.expand_field()
    path = gg.astar((0, 0), (gg.width - 1, gg.height - 1))
    result = gg.risk_sum(path)
    return result


if __name__ == "__main__":
    test()
    input = aocd.get_data(day=15, year=2021)
    print("Part One: ", part_one(input))
    print("Part Two: ", part_two(input))
