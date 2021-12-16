from collections import defaultdict
from typing import Dict, Tuple
import aocd
from bitstring import BitArray
from functools import reduce
import operator


OPERATIONS = {
    0: sum,
    1: lambda x: reduce(operator.mul, x, 1),
    2: min,
    3: max,
    5: lambda x: x[0] > x[1],
    6: lambda x: x[0] < x[1],
    7: lambda x: x[0] == x[1],
}


def bits_to_int(bits):
    return int(bits.bin, 2)


def parse_literal(packet: BitArray):
    literal_bits = ""
    cont = True
    i = 0
    while cont:
        cont = packet[i]
        literal_bits += packet[i + 1 : i + 5].bin
        i += 5
    value = int(literal_bits, 2)
    return value, i


def parse_operator(packet: BitArray):
    params = []
    version_sum = 0
    length_type_id = packet[0]
    if length_type_id:
        i = 12
        for _ in range(bits_to_int(packet[1:12])):
            value, vc, inc = parse_packet(packet[i:])
            params.append(value)
            version_sum += vc
            i += inc
    else:
        subpacket_length = bits_to_int(packet[1:16])
        i = 16
        while i - 16 < subpacket_length:
            value, vc, inc = parse_packet(packet[i:])
            params.append(value)
            version_sum += vc
            i += inc

    return params, version_sum, i


def parse_packet(packet: BitArray):
    version_sum = 0
    version_id = bits_to_int(packet[0:3])
    version_sum += version_id
    type_id = bits_to_int(packet[3:6])
    if type_id == 4:
        value, inc = parse_literal(packet[6:])
        return value, version_sum, inc + 6
    else:
        params, vc, inc = parse_operator(packet[6:])
        value = OPERATIONS[type_id](params)
        return value, version_sum + vc, inc + 6


def parse(transmission):
    packet = BitArray(hex=transmission)
    value, vc, _ = parse_packet(packet)
    return value, vc


def test():
    input = "D2FE28"
    v, r = parse(input)
    assert r == 6, r
    assert v == 2021, v

    input = "8A004A801A8002F478"
    v, r = parse(input)
    assert r == 16, r
    assert v == 15, v

    input = "620080001611562C8802118E34"
    v, r = parse(input)
    assert r == 12, r
    assert v == 46, v

    input = "C0015000016115A2E0802F182340"
    version_string, r = parse(input)
    assert r == 23, r
    assert v == 46, v

    input = "A0016C880162017C3686B18A3D4780"
    v, r = parse(input)
    assert r == 31, r
    assert v == 54, v


def part_one(input):
    _, r = parse(input)
    return r


def part_two(input):
    v, _ = parse(input)
    return v


if __name__ == "__main__":
    test()
    input = aocd.get_data(day=16, year=2021)
    print("Part One: ", part_one(input))
    print("Part Two: ", part_two(input))
