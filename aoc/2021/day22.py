"""
--- Day 22: Reactor Reboot ---
https://adventofcode.com/2021/day/22
"""

import aocd
import numpy as np
import parse

DATA = []
for switch, x1, x2, y1, y2, z1, z2 in parse.findall("{:w} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", aocd.data):
    DATA.append((switch, (x1, x2), (y1, y2), (z1, z2)))

cropped = []
for switch, x, y, z in DATA:
    x1 = max(-50, x[0]) + 50
    x2 = min(50, x[1]) + 50
    if x1 > x2:
        continue

    y1 = max(-50, y[0]) + 50
    y2 = min(50, y[1]) + 50
    if y1 > y2:
        continue

    z1 = max(-50, z[0]) + 50
    z2 = min(50, z[1]) + 50
    if z1 > z2:
        continue

    cropped.append((switch, (x1, x2), (y1, y2), (z1, z2)))

shape = tuple(max(e[i][1] for e in cropped) + 1 for i in range(1, 4))
reactor = np.zeros(shape, dtype=bool)
for switch, x, y, z in cropped:
    reactor[x[0]:x[1] + 1, y[0]:y[1] + 1, z[0]:z[1] + 1] = switch == "on"

print("Part One", np.count_nonzero(reactor))


class Line:
    def __init__(self, x1, x2):
        if x1 >= x2:
            raise ValueError('coordinates are invalid')
        self.x1 = x1
        self.x2 = x2

    def length(self):
        return self.x2 - self.x1

    def issubset(self, other):
        """ Report whether another line completely contains this line. """
        return other.x1 <= self.x1 <= other.x2 and other.x1 <= self.x2 <= other.x2

    def intersection(self, other):
        a, b = self, other
        x1 = max(min(a.x1, a.x2), min(b.x1, b.x2))
        x2 = min(max(a.x1, a.x2), max(b.x1, b.x2))
        if x1 < x2:
            return Line(x1, x2)

    __and__ = intersection


class Cuboid:
    def __init__(self, a: Line, b: Line, c: Line, weight=1):
        self.a = a
        self.b = b
        self.c = c
        self.weight = weight

    def area(self):
        return self.weight * self.a.length() * self.b.length() * self.c.length()

    def issubset(self, other):
        """ Report whether another cube completely contains this cube. """
        return self.a.issubset(other.a) and self.b.issubset(other.b) and self.c.issubset(other.c)

    def intersection(self, other):
        if (a := self.a & other.a) and (b := self.b & other.b) and (c := self.c & other.c):
            return Cuboid(a, b, c)

    __and__ = intersection


active = []
for switch, x, y, z in DATA:
    cuboid = Cuboid(Line(min(x), max(x) + 1), Line(min(y), max(y) + 1), Line(min(z), max(z) + 1))

    active[:] = [a for a in active if not a.issubset(cuboid)]  # filter all the active cuboids completely contained

    intersections = []
    for a in active:
        if inter := cuboid & a:
            inter.weight = -a.weight  # the intersection gets the opposite weight
            intersections.append(inter)

    if switch == "on":
        active.append(cuboid)
    active.extend(intersections)

print(f"The reactor model contains {len(active)} cuboids; the sequence contains {len(DATA)}.")
print("Part Two", sum(map(Cuboid.area, active)))
