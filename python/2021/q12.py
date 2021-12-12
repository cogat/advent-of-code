import aocd
from collections import defaultdict
from typing import List, Dict


class Graph:
    def __init__(self, input_lines):
        self.nodes = defaultdict(list)
        for line in input_lines:
            lhs, rhs = line.strip().split("-")
            self.nodes[lhs].append(rhs)
            self.nodes[rhs].append(lhs)

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        paths = []

        def _can_visit(node):
            if node.lower() != node:
                return True
            if node not in path:
                return True
            return False

        for node in self.nodes[start]:
            if _can_visit(node):
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_all_paths_with_one_revisit(
        self,
        start,
        end,
        path=[],
    ):
        path = path + [start]
        if start == end:
            return [path]
        paths = []

        def _can_visit(node):
            if (node.lower() != node) or (node not in path):
                return True
            if (node.lower() == node) and (node not in ("start", "end")):
                # allow the small cave node if no other lowercase node appears > 1 time
                # Horrendously inefficient, but works. For faster results pass around a dict
                # that tallies each node's uses.
                for small_cave in {p for p in path if p.lower() == p}:
                    if path.count(small_cave) > 1:
                        return False
                return True

            return False

        for node in self.nodes[start]:
            can_visit = _can_visit(node)
            if can_visit:
                newpaths = self.find_all_paths_with_one_revisit(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)

        return paths


def part_one(input_lines):
    graph = Graph(input_lines)
    return len(graph.find_all_paths("start", "end"))


def part_two(input_lines):
    graph = Graph(input_lines)
    return len(graph.find_all_paths_with_one_revisit("start", "end"))


def test():
    input = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    graph = Graph(input.splitlines())
    result_one = len(graph.find_all_paths("start", "end"))
    assert result_one == 10, result_one
    result_two = len(graph.find_all_paths_with_one_revisit("start", "end"))
    assert result_two == 36, result_two


if __name__ == "__main__":
    test()
    lines = aocd.get_data(day=12, year=2021).splitlines()
    print(part_one(lines))
    print(part_two(lines))
