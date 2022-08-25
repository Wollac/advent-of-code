"""
--- Day 5: Hydrothermal Venture ---
https://adventofcode.com/2021/day/5
"""
import re
from collections import defaultdict

import aocd

DATA = [[int(n) for n in re.match(r"(\d*),(\d*) -> (\d*),(\d*)", line).groups()] for line in aocd.data.splitlines()]

grid = defaultdict(int)
for x1, y1, x2, y2 in DATA:
    if y1 == y2:  # horizontal
        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid[x, y1] += 1
    elif x1 == x2:  # vertical
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[x1, y] += 1

print("Part One:", sum(n > 1 for n in grid.values()))

for x1, y1, x2, y2 in DATA:
    if x1 != x2 and y1 != y2:  # diagonal
        if x1 < x2:
            for x in range(x1, x2 + 1):
                if y1 < y2:
                    grid[x, x - x1 + y1] += 1
                else:
                    grid[x, y1 - (x - x1)] += 1
        else:
            for x in range(x2, x1 + 1):
                if y2 < y1:
                    grid[x, x - x2 + y2] += 1
                else:
                    grid[x, y2 - (x - x2)] += 1

print("Part Two:", sum(n > 1 for n in grid.values()))
