"""
--- Day 14: Extended Polymerization ---
https://adventofcode.com/2021/day/14
Start: 12:03 Part 1: 12:12 Part 2: 12:32
"""
from collections import Counter

import aocd
from parse import findall

TEMPLATE, _, RULES = aocd.data.partition('\n')
RULES = {p: e for p, e in findall("{:w} -> {:l}", RULES)}

# Part One
# Create a list of template elements and then insert an element for each matched pair.

lst = list(TEMPLATE)
for _ in range(10):
    i = 1
    while i < len(lst):
        pair = lst[i - 1] + lst[i]
        if pair in RULES:
            lst.insert(i, RULES[pair])
            i += 1
        i += 1
print(f"The length of the polymer is {len(lst)}.")

elements = Counter(lst)
print("Part One", max(elements.values()) - min(elements.values()))

# Part Two
# Instead of trying to construct the complete polymer in every step, we count occurrences of individual pairs.
# A match then completely removes a pair and creates new occurrences of the two new corresponding pairs.

pairs = Counter(a + b for a, b in zip(TEMPLATE, TEMPLATE[1:]))  # count individual pairs in the template
for _ in range(40):
    for pair, count in pairs.copy().items():
        if pair in RULES:
            pairs[pair] -= count
            pairs[pair[0] + RULES[pair]] += count
            pairs[RULES[pair] + pair[1]] += count

# all the pairs are overlapping, thus to count the chars we need to count the first character in the result
# and then the second char of each pair
elements = Counter(TEMPLATE[0])
for pair, count in pairs.items():
    elements[pair[1]] += count

print(f"The length of the polymer is {sum(elements.values())}.")
print("Part Two", max(elements.values()) - min(elements.values()))
