"""
--- Day 3: Binary Diagnostic ---
https://adventofcode.com/2021/day/3
"""
from itertools import count

import aocd
import numpy as np

DATA = np.array([[int(c) for c in line] for line in aocd.data.splitlines()])

# for every bit go with the majority
majority = np.where(np.sum(DATA, axis=0) > len(DATA) / 2.0, '1', '0')

gamma = int("".join(majority), 2)
epsilon = ~(~0 << len(majority) | gamma)  # invert gama

print("Part One", gamma * epsilon)

# Part Two

a = np.copy(DATA)
for i in count():
    col = a[:, i]
    # select rows where i-th column is the majority
    a = a[col == int(sum(col) >= len(a) / 2.0)]
    if len(a) == 1:
        break

generator = int("".join(map(str, a[0])), 2)

a = np.copy(DATA)
for i in count():
    col = a[:, i]
    # select rows where i-th column is not the majority
    a = a[col == int(sum(col) < len(a) / 2.0)]
    if len(a) == 1:
        break

scrubber = int("".join(map(str, a[0])), 2)

print("Part Two", generator * scrubber)
