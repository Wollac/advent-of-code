"""
--- Day 19: Tractor Beam ---
https://adventofcode.com/2019/day/19
"""
import bisect

import aocd

from .intcode import IntComputer

PROGRAM = [int(n) for n in aocd.data.split(",")]


def beam(x, y):
    comp = IntComputer(PROGRAM, (x, y))
    return comp.run().pop()


area = {}
x0 = 0
for y in range(50):
    on = False
    for x in range(x0, 50):
        v = beam(x, y)
        area[x, y] = v
        if not on and v:
            on = True
            x0 = x
        if on and not v:
            break

for y in range(50):
    print("".join(['#' if area.get((x, y), 0) else '.' for x in range(50)]))
print("Part One:", sum(area.values()))


# dict with "compute if missing"
class ComputeDict(dict):
    def __init__(self, factory):
        super(ComputeDict, self).__init__()
        self.factory = factory

    def __missing__(self, key):
        self[key] = value = self.factory(key)
        return value


def first_x(y, gradient):
    x = int(y / gradient)
    while x > 0 and beam(x, y):
        x -= 1
    while not beam(x, y):
        x += 1
    return x


def find(width, gradient):
    d = width - 1

    def check(y):
        if y < d:
            return False
        x0 = first_x(y, gradient)
        return beam(x0 + d, y - d) != 0

    y0 = bisect.bisect_left(ComputeDict(check), True, d, 10000)
    return first_x(y0, gradient), y0 - d


m = 50 / x0
m = 10000 / first_x(10000, m)
print("estimated gradient:", m)

x, y = find(100, m)
print("Part Two:", x * 10000 + y)
