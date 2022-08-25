"""
--- Day 11: Dumbo Octopus ---
https://adventofcode.com/2021/day/11
Start: 5:54 Part 1: 05:59 Part 2: 06:04
"""
import aocd
import numpy as np

levels = np.array([[int(c) for c in line] for line in aocd.data.splitlines()])
neighbors = [(1, 0), (1, 1), (0, 1), (0, -1), (-1, -1), (-1, 0), (1, -1), (-1, 1)]
size = levels.size

flashes = 0
for step in range(1, 1000):
    levels += 1
    while (flashing := (levels > 9)).any():
        # for each flashing cell, increment its neighbor levels
        for i, j in np.argwhere(flashing):
            for n in neighbors:
                di, dj = i + n[1], j + n[0]
                if 0 <= di < levels.shape[0] and 0 <= dj < levels.shape[1]:
                    levels[di, dj] += 1
            levels[i, j] = -size  # set flashed cells to a low values that no number of flashes can increase it to 0

    flashed = levels < 0
    if flashed.all():
        print("Part Two", step)
        break

    flashes += np.count_nonzero(flashed)
    levels[flashed] = 0
    if step == 100:
        print("Part One", flashes)
