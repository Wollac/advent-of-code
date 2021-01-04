"""
--- Day 20: Jurassic Jigsaw ---
https://adventofcode.com/2020/day/20
"""
import math
import re

import aocd
import numpy as np

DATA = {int(i): np.array([[c == '#' for c in line] for line in tile_raw.splitlines()])
        for i, tile_raw, _ in re.findall(r"Tile (\d+):\s+(([.#]+\n?)+)", aocd.data)}
N = math.isqrt(len(DATA))


# Part One

def transform(m):
    for k in range(4):
        yield np.rot90(m, k)
    m = np.flipud(m)
    for k in range(4):
        yield np.rot90(m, k)


# all tiles in all orientations
options = {i: [t for t in transform(m)] for i, m in DATA.items()}


# solve using backtracking
def bt(p, ids, tiles):
    if p >= len(ids.flat):
        return True
    x, y = np.unravel_index(p, ids.shape)
    for i, opt in options.items():
        if i in ids:
            continue

        ids[y, x] = i
        for tile in opt:
            # check borders
            if x > 0 and not np.array_equal(tiles[ids[y, x - 1]][:, -1], tile[:, 0]):
                continue
            if y > 0 and not np.array_equal(tiles[ids[y - 1, x]][-1, :], tile[0, :]):
                continue

            tiles[i] = tile
            if bt(p + 1, ids, tiles):
                return True
        ids[y, x] = 0
    return False


ids = np.zeros((N, N), dtype=int)
tiles = {}
if not bt(0, ids, tiles):
    raise Exception("infeasible")

sol1 = ids[0, 0] * ids[0, -1] * ids[-1, 0] * ids[-1, -1]
print("Part One: The product of the IDs of the four corner tiles is", sol1)


# Part Two

def findall(patterns, strings):
    result = []
    for y in range(len(strings) - len(patterns)):
        start = 0
        while m := patterns[0].search(strings[y], start):
            start = m.start()
            if all(pattern.match(strings[y + i], start) for i, pattern in enumerate(patterns)):
                result.append((start, y))
            start += 1
    return result


monster_raw = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
monster_pattern = [re.compile(m.replace(" ", ".")) for m in monster_raw]

# stitch the image together without borders
image = np.vstack(tuple(np.hstack(tuple(tiles[i][1:-1, 1:-1] for i in row)) for row in ids))

for t in transform(image):
    if monsters := findall(monster_pattern, ["".join(map(lambda b: '#' if b else '.', r)) for r in t]):
        break

sol2 = np.count_nonzero(image) - len(monsters) * sum(row.count("#") for row in monster_raw)
print("Part Two: The number of '#'s that are not part of a sea monster is", sol2)
