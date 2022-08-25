"""
--- Day 13: Transparent Origami ---
https://adventofcode.com/2021/day/13
Start: 04:29 Part 1: 04:42 Part 2: 05:01
"""
import aocd
import numpy as np
from parse import findall

DOTS = list(findall('{:d},{:d}', aocd.data))
FOLDS = list(findall('{:l}={:d}', aocd.data))

# the dimensions of the paper correspond to the double of the first fold position
shape = (
    next(n for axis, n in FOLDS if axis == 'y') * 2 + 1,
    next(n for axis, n in FOLDS if axis == 'x') * 2 + 1,
)
# model the paper as a boolean matrix, where True corresponds to a dot
P = np.zeros(shape, dtype=bool)
for x, y in DOTS:
    P[y, x] = True

print(f"The {P.shape[1]}x{P.shape[0]} paper is marked with {np.count_nonzero(P)} dots.")


def fold(a, axis, n):
    if axis == 'y':
        assert n == (a.shape[0] - 1) // 2  # we always fold in half
        return (a | np.flipud(a))[:n, :]
    if axis == 'x':
        assert n == (a.shape[1] - 1) // 2  # we always fold in half
        return (a | np.fliplr(a))[:, :n]


# count the visible dots after the first fold
print("Part One", np.count_nonzero(fold(P, *FOLDS[0])))

for axis, n in FOLDS:
    P = fold(P, axis, n)

# pretty print the dots after all folds
for row in np.where(P, "█", " "):
    print("".join(row))
