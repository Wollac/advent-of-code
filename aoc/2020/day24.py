"""
--- Day 24: Lobby Layout ---
https://adventofcode.com/2020/day/24
"""
import re

import aocd

pattern = re.compile(r"e|se|sw|w|nw|ne")

DATA = [[step for step in pattern.findall(line)] for line in aocd.data.splitlines()]

# Part One

D = {"e": (1, 1), "se": (0, 1), "sw": (-1, 0), "w": (-1, -1), "nw": (0, -1), "ne": (1, 0)}

black_tiles = set()
for steps in DATA:
    p = (0, 0)
    for step in steps:
        p = (p[0] + D[step][0], p[1] + D[step][1])
    black_tiles ^= {p}

print("Part One: The number of tiles with the black side up is", len(black_tiles))

# Part Two

for _ in range(100):
    neighboring_tiles = {(p[0] + n[0], p[1] + n[1]) for p in black_tiles for n in D.values()}

    tmp = set()
    for p in neighboring_tiles:
        n_black = sum((p[0] + n[0], p[1] + n[1]) in black_tiles for n in D.values())
        if p in black_tiles:
            if 0 < n_black <= 2:
                tmp.add(p)
        else:
            if n_black == 2:
                tmp.add(p)
    black_tiles = tmp

print("Part Two: The number of black tiles after 100 days is", len(black_tiles))
