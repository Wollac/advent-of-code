"""
--- Day 12: The N-Body Problem ---
https://adventofcode.com/2019/day/12
"""
import re
from itertools import count

import aocd
import numpy as np

DATA = np.array(re.findall(r"x=(-?\d+), y=(-?\d+), z=(-?\d+)", aocd.data), dtype=int)


def do_step(positions, velocities):
    # velocities += [sum(np.sign(b - a) for b in positions) for a in positions]
    velocities += np.sum(np.sign(positions - positions[:, np.newaxis]), axis=1)
    positions += velocities


positions = np.copy(DATA)
velocities = np.zeros_like(positions)
for _ in range(1000):
    do_step(positions, velocities)

energy = (np.sum(np.abs(positions), axis=1) * np.sum(np.abs(velocities), axis=1)).sum()
print("Part One:", energy)

cycles = []
for axis, positions in enumerate(np.transpose(DATA)):
    velocities = np.zeros_like(positions)
    initial_state = (tuple(positions), tuple(velocities))
    for step in count(1):
        do_step(positions, velocities)
        if (tuple(positions), tuple(velocities)) == initial_state:
            break
    print(f"{'XYZ'[axis]}-cycle of {step} steps")
    cycles.append(step)

print("Part Two: The LCM of all the cycles is", np.lcm.reduce(cycles))
