"""
--- Day 8: Seven Segment Search ---
https://adventofcode.com/2021/day/8
"""
import math

import aocd
import networkx as nx

area = [[int(c) for c in line] for line in aocd.data.splitlines()]


def neighbors(a, x, y, d=1):
    return [a[j][i] for j in range(max(y - d, 0), min(y + d + 1, len(a)))
            for i in range(max(x - d, 0), min(x + d + 1, len(a[0]))) if i != x or j != y]


print("Part One", sum(h + 1 for y, row in enumerate(area) for x, h in enumerate(row) if h < min(neighbors(area, x, y))))

# create the undirected flow graph
G = nx.Graph()
for y, row in enumerate(area):
    for x, h in enumerate(row):
        if h == 9:  # locations of height 9 do not count as being in any basin
            continue
        if y > 0 and area[y - 1][x] != 9:
            G.add_edge((x, y - 1), (x, y))
        if x > 0 and area[y][x - 1] != 9:
            G.add_edge((x - 1, y), (x, y))

# now basins correspond to the connected components in the graph
basins = sorted(nx.connected_components(G), key=len, reverse=True)

print(f"There are {len(basins)} basins, the largest basin has a size of {len(basins[0])}.")
print("Part Two", math.prod(len(c) for c in basins[:3]))
