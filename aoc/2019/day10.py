"""
--- Day 10: Monitoring Station ---
https://adventofcode.com/2019/day/10
"""
import math
from collections import deque
from itertools import groupby

import aocd

asteroids = [(x, y) for y, row in enumerate(aocd.data.splitlines()) for x, cell in enumerate(row) if cell == "#"]
print("Number of asteroids:", len(asteroids))


# Return the angle between a and b. Such that up is 0 and increasing clockwise.
def angle(a, b):
    x, y = b[0] - a[0], b[1] - a[1]
    return (math.atan2(y, x) + math.pi / 2) % (math.pi * 2)  # rotate 90° clockwise


visibility = {a: len({angle(a, b) for b in asteroids if b is not a}) for a in asteroids}
a0, sol1 = max(visibility.items(), key=lambda kv: kv[1])

print(f"Asteroid at {a0} can detect {sol1} other asteroids.")
print("Part One:", sol1)

# group the asteroids by their angle, the groups sorted by distance
angles = {a: angle(a0, a) for a in asteroids if a is not a0}
groups = deque(sorted(asteroids, key=lambda a: math.dist(a0, a), reverse=True) for _, asteroids in
               groupby(sorted(angles, key=angles.get), key=angles.get))

order = []
while groups:
    group = groups.popleft()
    order.append(group.pop())
    if group:
        groups.append(group)

sol2 = order[199]
print(f"The 200th asteroid to be vaporized is at {sol2}.")
print("Part Two:", sol2[0] * 100 + sol2[1])
