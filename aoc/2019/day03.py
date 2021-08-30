"""
--- Day 3: Crossed Wires ---
https://adventofcode.com/2019/day/3
"""
import aocd

paths = [[(c[0], int(c[1:])) for c in line.split(",")] for line in aocd.data.splitlines()]

D = {"R": (1, 0), "U": (0, -1), "L": (-1, 0), "D": (0, 1)}

coordinates = []
for path in paths:
    V = {}
    v = (0, 0)
    length = 0
    for c, n in path:
        for _ in range(n):
            v = (v[0] + D[c][0], v[1] + D[c][1])
            length += 1
            if v not in V:
                V[v] = length
    coordinates.append(V)

intersections = set(coordinates[0]).intersection(coordinates[1])

sol1 = min(abs(x) + abs(y) for x, y in intersections)
print("Part One:", sol1)

sol2 = min(coordinates[0][v] + coordinates[1][v] for v in intersections)
print("Part Two:", sol2)
