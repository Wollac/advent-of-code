"""
--- Day 25: Sea Cucumber ---
https://adventofcode.com/2021/day/25
"""
import aocd
import numpy as np

G = np.array([list(line) for line in aocd.data.splitlines()])
Y, X = G.shape

i = 0
while True:
    i += 1

    modified = False
    G2 = G.copy()
    for y, x in np.argwhere(G == ">"):
        x2 = (x + 1) % X
        if G[y][x2] == ".":
            modified = True
            G2[y][x] = "."
            G2[y][x2] = ">"
    G[:] = G2

    for y, x in np.argwhere(G2 == "v"):
        y2 = (y + 1) % Y
        if G2[y2][x] == ".":
            modified = True
            G[y][x] = "."
            G[y2][x] = "v"

    if not modified:
        break

print("Part One", i)
