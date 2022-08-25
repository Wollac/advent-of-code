"""
--- Day 19: Beacon Scanner ---
https://adventofcode.com/2021/day/19
Start: 07:23 Part 1: 09:07 Part 2: 09:17
"""
import itertools
import math
from collections import Counter

import aocd
import numpy as np
from scipy.spatial.distance import cityblock

scans = []
for block in aocd.data.split("\n\n"):
    scans.append(np.array([list(map(int, beacon.split(","))) for beacon in block.partition("\n")[2].splitlines()]))


def rot_x(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[1, 0, 0],
                     [0, c, -s],
                     [0, s, c]])


def rot_y(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, 0, s],
                     [0, 1, 0],
                     [-s, 0, c]])


def rot_z(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s, 0],
                     [s, c, 0],
                     [0, 0, 1]])


def rot90(i, j, k):
    return (rot_x(math.pi / 2 * i) @ rot_y(math.pi / 2 * j) @ rot_z(math.pi / 2 * k)).astype(int)


# create list of all unique 90° rotation matrices
ROTS = list({repr(rot := rot90(i, j, k)): rot for i, j, k in np.ndindex(4, 4, 4)}.values())
assert len(ROTS) == 24


def overlap(i, j):
    # try all possible rotations of scanner j
    for ori, rot in enumerate(ROTS):
        # rotate all the beacons of scanner j
        rotated = np.matmul(scans[j], rot.T)  # [np.matmul(rot, e) for e in DATA[j]]
        # for each pair of coordinates compute the position of scanner j (relative to scanner i) under the assumption
        # that the coordinates correspond to the same beacon and count the different positions
        scanner_positions = Counter(tuple(beacon_a - beacon_b) for beacon_a in scans[i] for beacon_b in rotated)
        # determine the position of scanner j that has the largest number of overlapping beacons
        pos, count = scanner_positions.most_common(1)[0]
        if count >= 12:  # the scanners i and j overlap, if there are at least 12 matching beacon pairs
            return pos, ori


def transform(pos, ori, sequence):
    for e in sequence:
        yield tuple(np.matmul(ROTS[ori], e) + pos)


def search(anchor, processed: set) -> (set, list):
    beacons, scanners = set(), []
    for i, scan in enumerate(scans):
        if i in processed:
            continue
        if m := overlap(anchor, i):
            pos, ori = m
            scanners.append(pos)
            beacons.update(transform(pos, ori, scan))
            processed.add(i)

            b, s = search(i, processed)
            beacons.update(transform(pos, ori, b))
            scanners.extend(transform(pos, ori, s))

    return beacons, scanners


beacons, scanners = search(0, set())

print("Part One", len(beacons))
print("Part Two", max(cityblock(scanner_a, scanner_b) for scanner_a, scanner_b in itertools.permutations(scanners, 2)))
