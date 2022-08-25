"""
--- Day 8: Seven Segment Search ---
https://adventofcode.com/2021/day/8
"""
from itertools import permutations

import aocd

DATA = [tuple(s.split() for s in line.split("|")) for line in aocd.data.splitlines()]
DIGITS = {"abcefg": '0', "cf": '1', "acdeg": '2', "acdfg": '3', "bcdf": '4',
          "abdfg": '5', "abdefg": '6', "acf": '7', "abcdefg": '8', "abcdfg": '9'}

# loop through all provided digits and count the easy ones
print("Part One", sum(sum(len(digit) in (2, 3, 4, 7) for digit in digits) for _, digits in DATA))


# Part Two
# instead of relying on easy digits and deducing more from this,
# we brute-force all the possible mapping and check when this leads to valid digits

# apply the mapping between signal wires and segments to the pattern
def apply(mapping: dict, pattern: str) -> str:
    return "".join(sorted(map(mapping.get, pattern)))


# each permutation corresponds to a potential mapping
mappings = [{a: b for a, b in zip(perm, "abcdefg")} for perm in permutations("abcdefg")]

decoded = []
for patterns, digits in DATA:
    for m in mappings:
        if all(apply(m, pattern) in DIGITS for pattern in patterns):
            decoded.append(int("".join([DIGITS[apply(m, digit)] for digit in digits])))
            break

print("Part Two", sum(decoded))
