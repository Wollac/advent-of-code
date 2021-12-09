"""
--- Day 11: Space Police ---
https://adventofcode.com/2019/day/11
"""
from collections import defaultdict

import aocd

from .intcode import IntComputer

program = [int(n) for n in aocd.data.split(",")]


def paint(canvas):
    robot = IntComputer(program)
    pos = (0, 0)
    heading = (0, -1)  # up
    try:
        while True:
            robot.input.append(canvas[pos])
            canvas[pos] = robot.run(IntComputer.op_output).popleft()
            rot = robot.run(IntComputer.op_output).popleft()
            if rot == 0:
                heading = (heading[1], -heading[0])
            elif rot == 1:
                heading = (-heading[1], heading[0])
            else:
                raise Exception(f"invalid rotation '{rot}'")
            pos = (pos[0] + heading[0], pos[1] + heading[1])
    except IntComputer.Halt:
        return


hull = defaultdict(int, {(0, 0): 0})
paint(hull)
print("Part One:", len(hull))

hull = defaultdict(int, {(0, 0): 1})
paint(hull)

x_lo, x_high = min(p[0] for p in hull), max(p[0] for p in hull)
y_lo, y_high = min(p[1] for p in hull), max(p[1] for p in hull)
image = [[hull[(x, y)] for x in range(x_lo, x_high + 1)] for y in range(y_lo, y_high + 1)]
for row in image:
    print("".join("█" if c else " " for c in row))
