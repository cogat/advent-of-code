import aocd
from collections import defaultdict

working_digits = {
    "0": "abc efg",  # 6:
    "1": "  c  f ",  # 2: UNIQUE length
    "2": "a cde g",  # 5: only one that is missing f also misses *b*
    "4": " bcd f ",  # 4: UNIQUE length
    "3": "a cd fg",  # 5:
    "5": "ab d fg",  # 5: missing c and ambiguous *e*
    "6": "ab defg",  # 6: missing only c
    "7": "a c  f ",  # 3: UNIQUE length
    "8": "abcdefg",  # 7: UNIQUE length
    "9": "abcd fg",  # 6:
    # frequency of signals the above, for disambiguation
    #     8687497
}

# transpose the above
signal_to_digit = {v.replace(" ", ""): k for k, v in working_digits.items()}


def part_one(data):
    return sum([sum(1 for x in line[-1] if len(x) in (2, 4, 3, 7)) for line in data])


def find_mapping(digit_signals):
    M = {}
    # tally the frequency of each letter in the input data:
    frequency_tally = defaultdict(int)
    # count the length of tokens each letter appears in
    length_tally = defaultdict(set)
    for signal in digit_signals:
        length = len(signal)
        for line in signal:
            frequency_tally[line] += 1
            length_tally[line].add(length)

    # transpose frequency_tally:
    frequency_to_candidates = defaultdict(set)
    for k, v in frequency_tally.items():
        frequency_to_candidates[v].add(k)

    # these have unique frequencies
    M[frequency_to_candidates[6].pop()] = "b"
    M[frequency_to_candidates[4].pop()] = "e"
    M[frequency_to_candidates[9].pop()] = "f"

    # to distinguish a and c
    # c is the one that appears in the signal of length 2
    c1, c2 = tuple(frequency_to_candidates[8])
    if 2 in length_tally[c1]:
        M[c1], M[c2] = "ca"
    else:
        M[c1], M[c2] = "ac"

    # now to distinguish d and g
    # d is the one that appears in the signal of length 4
    c3, c4 = tuple(frequency_to_candidates[7])
    if 4 in length_tally[c3]:
        M[c3], M[c4] = "dg"
    else:
        M[c3], M[c4] = "gd"

    return M


def apply_mapping(mapping, digit_signals):
    return int(
        "".join(
            [
                signal_to_digit["".join(sorted(list({mapping[d] for d in signal})))]
                for signal in digit_signals
            ]
        )
    )


def part_two(data):
    return sum(apply_mapping(find_mapping(lhs), rhs) for lhs, rhs in data)


def test():
    lhs = [set(x) for x in "dbcfeag cgaed fe bfgad aefcdb efa efgda gcef dcaebg dfeagc".split()]
    mapping = find_mapping(lhs)
    assert mapping == {
        "a": "a",
        "b": "e",
        "c": "b",
        "d": "g",
        "e": "f",
        "f": "c",
        "g": "d",
    }, mapping

    rhs = [set(x) for x in "fae cfge fae baefdc".split()]
    digits = apply_mapping(mapping, rhs)
    assert digits == 7470, digits


if __name__ == "__main__":
    test()
    lines = aocd.get_data(day=8, year=2021).splitlines()
    pre_and_posts = [line.split(" | ") for line in lines]
    data = [[[set(y) for y in x.split()] for x in item] for item in pre_and_posts]
    # print(data)

    print(part_one(data))
    print(part_two(data))
