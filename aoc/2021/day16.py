"""
--- Day 16: Packet Decoder ---
https://adventofcode.com/2021/day/16
Start: 07:06 Part 1: 08:01 Part 2: 08:11
"""
from collections import namedtuple
from functools import reduce

import aocd

# convert to binary and revert the bits so that pop() returns the first bit
bits = [(int(c, 16) >> (3 - i)) & 1 for c in aocd.data for i in range(4)][::-1]
print(f"The input consists of {len(bits)} bits.")

Packet = namedtuple("Packet", ["version", "type", "data"])


def parse_int(buffer: list, nbits: int) -> int:
    return reduce(lambda v, e: (v << 1) | e, (buffer.pop() for _ in range(nbits)))


def parse_varint(buffer: list):
    v = 0
    last = False
    while not last:
        last = not buffer.pop()
        v = (v << 4) | parse_int(buffer, 4)
    return v


def parse_sub(buffer: list):
    length_type_id = parse_int(buffer, 1)

    if length_type_id == 0:
        length = parse_int(buffer, 15)
        target = len(buffer) - length
        packets = []
        while len(buffer) != target:  # parse until length bits have been read
            packets.append(parse_packet(buffer))
        return packets

    if length_type_id == 1:
        num = parse_int(buffer, 11)
        return [parse_packet(buffer) for _ in range(num)]


def parse_packet(buffer: list) -> Packet:
    version = parse_int(buffer, 3)
    type_id = parse_int(buffer, 3)
    if type_id == 4:
        return Packet(version, type_id, parse_varint(buffer))
    else:
        return Packet(version, type_id, parse_sub(buffer))


def sum_versions(p: Packet):
    s = p.version
    if p.type != 4:
        s += sum(sum_versions(sub) for sub in p.data)
    return s


outer = parse_packet(bits)
print(outer)
print("Part One", sum_versions(outer))

OPERATOR = {0: lambda a, b: a + b, 1: lambda a, b: a * b, 2: min, 3: max,
            5: lambda a, b: int(a > b), 6: lambda a, b: int(a < b), 7: lambda a, b: int(a == b)}


def evaluate(p: Packet):
    if p.type == 4:
        return p.data
    return reduce(OPERATOR[p.type], map(evaluate, p.data))


print("Part Two", evaluate(outer))
