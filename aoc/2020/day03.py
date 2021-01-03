"""
--- Day 3: Toboggan Trajectory ---
https://adventofcode.com/2020/day/3
"""
from math import prod

import aocd

DATA = []
for line in aocd.data.splitlines():
    row = []
    for c in line.strip():
        if c == '#':
            row.append(True)
        elif c == '.':
            row.append(False)
        else:
            raise ValueError("invalid character '%c' in line %d" % (c, len(DATA) + 1))
    DATA.append(row)
    if len(row) != len(DATA[0]):
        raise ValueError("invalid length of line %d" % len(DATA))


def count(vector, area):
    s = 0
    x = y = 0
    while True:
        y += vector[1]
        if y >= len(area):
            break
        x = (x + vector[0]) % len(area[y])
        if area[y][x]:
            s += 1
    return s


# Part One

sol1 = count((3, 1), DATA)
print("Part One: The number of encountered trees is %d" % sol1)

# Part Two

sol2 = prod(count(slope, DATA) for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])
print("Part Two: The product of the number of trees encountered on each slope is %d" % sol2)
