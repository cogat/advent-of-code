import aocd
from collections import defaultdict


class Polymer:
    def __init__(self, *, string, rules):
        self.rules = rules
        self.pair_freqs = defaultdict(int)
        for index in range(len(string) - 1):
            self.pair_freqs[string[index : index + 2]] += 1
        self.last_letter = string[-1]

    def apply_rules(self, times=1):
        for n in range(times):
            new_pair_freqs = defaultdict(int)
            for pair, count in self.pair_freqs.items():
                new_char = self.rules[pair]
                new_pair_freqs[pair[0] + new_char] += count
                new_pair_freqs[new_char + pair[1]] += count
            self.pair_freqs = new_pair_freqs

    def get_letter_freqs(self):
        stats = defaultdict(int)
        for pair, count in self.pair_freqs.items():
            stats[pair[0]] += count
        stats[self.last_letter] += 1
        return stats

    def most_common_minus_least_common(self):
        sorted_stats = sorted(self.get_letter_freqs().items(), key=lambda item: item[1])
        return sorted_stats[-1][1] - sorted_stats[0][1]


def get_string_and_rules(input):
    string, rules = input.split("\n\n")
    return string, dict([line.split(" -> ") for line in rules.splitlines()])


def test():
    input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

    string, rules = get_string_and_rules(input)
    assert string == "NNCB"
    assert len(rules) == 16
    p = Polymer(string=string, rules=rules)
    p.apply_rules(times=2)
    assert p.get_letter_freqs() == {
        "N": 2,
        "C": 4,
        "B": 6,
        "H": 1,
    }, p.get_letter_freqs()
    p.apply_rules(times=8)
    result = p.most_common_minus_least_common()
    assert result == 1588, result


def part_one(input):
    string, rules = get_string_and_rules(input)
    p = Polymer(rules=rules, string=string)
    p.apply_rules(times=10)
    return p.most_common_minus_least_common()


def part_two(input):
    string, rules = get_string_and_rules(input)
    p = Polymer(rules=rules, string=string)
    p.apply_rules(times=40)
    return p.most_common_minus_least_common()


if __name__ == "__main__":
    test()
    input = aocd.get_data(day=14, year=2021)
    print(part_one(input))
    print(part_two(input))
