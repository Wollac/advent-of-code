"""
--- Day 12: Rain Risk ---
https://adventofcode.com/2020/day/12
"""
import re

import aocd
import numpy as np

DATA = [(c, int(d)) for c, d in re.findall(r"([NSEWLRF])(\d+)", aocd.data)]
DIRS = [np.array(d) for d in [[1, 0], [0, 1], [-1, 0], [0, -1]]]

# Part One

pos = np.array([0, 0])
orientation = 0

for c, d in DATA:
    if c == 'E':
        pos += d * DIRS[0]
    elif c == 'S':
        pos += d * DIRS[1]
    elif c == 'W':
        pos += d * DIRS[2]
    elif c == 'N':
        pos += d * DIRS[3]
    elif c == 'R':
        orientation += d
    elif c == 'L':
        orientation -= d
    elif c == 'F':
        pos += d * DIRS[(orientation // 90) % 4]

print("The ship is at position (%d, %d)" % (pos[0], pos[1]))
norm = abs(pos[0]) + abs(pos[1])
print("Part One: The distance travelled is %d" % norm)


# Part Two

def rotate(d, point):
    c = (d // 90) % 4
    if c > 0:
        for _ in range(c):
            point[0], point[1] = -point[1], point[0]
    if c < 0:
        for _ in range(-c):
            point[0], point[1] = point[1], -point[0]


pos = np.array([0, 0])
waypoint = np.array([10, -1])

for c, d in DATA:
    if c == 'E':
        waypoint += d * DIRS[0]
    elif c == 'S':
        waypoint += d * DIRS[1]
    elif c == 'W':
        waypoint += d * DIRS[2]
    elif c == 'N':
        waypoint += d * DIRS[3]
    elif c == 'R':
        rotate(d, waypoint)
    elif c == 'L':
        rotate(-d, waypoint)
    elif c == 'F':
        pos += d * waypoint

print("The ship is at position (%d, %d)" % (pos[0], pos[1]))
norm = abs(pos[0]) + abs(pos[1])
print("Part Two: The distance travelled is %d" % norm)
