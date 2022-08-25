"""
--- Day 15: Chiton ---
https://adventofcode.com/2021/day/15
Start: 11:06 Part 1: 11:26 Part 2: 11:36
"""
import heapq
import sys

import aocd
import numpy as np

DATA = np.array([[int(i) for i in line] for line in aocd.data.splitlines()])
N = len(DATA)


# run a simplified dijkstra directly on the grid
def dijkstra(grid: np.ndarray):
    q = [(0, (0, 0))]
    distance = np.ones(grid.shape, dtype=int) * sys.maxsize
    distance[0, 0] = 0
    while q:
        dist, (i, j) = heapq.heappop(q)
        if i == grid.shape[0] - 1 and j == grid.shape[1] - 1:  # target reached
            return dist
        for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):  # one step horizontally/vertically
            v = (i + di, j + dj)
            if 0 <= v[0] < grid.shape[0] and 0 <= v[1] < grid.shape[1]:  # within the grid
                alt = dist + grid[v]  # the new distance equals the old distance plus the value of the new cell
                if alt < distance[v]:
                    distance[v] = alt
                    heapq.heappush(q, (alt, v))  # as all in-edges of a node have equal weight, there will be no updates


print("Part One", dijkstra(DATA))

extended = np.zeros((N * 5, N * 5), dtype=int)
for i in range(5):
    for j in range(5):
        tile = (DATA + (i + j))
        extended[i * N:i * N + N, j * N:j * N + N] = np.where(tile > 9, tile % 9, tile)

print("Part Two", dijkstra(extended))
