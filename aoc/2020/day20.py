"""
--- Day 20: Jurassic Jigsaw ---
https://adventofcode.com/2020/day/20
"""
import math

import aocd
import numpy as np
import regex as re

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

# stitch the image together without borders
image = np.vstack(tuple(np.hstack(tuple(tiles[id][1:-1, 1:-1] for id in row)) for row in ids))

monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
# make the monster a regex pattern
monster_pattern = f"[.#\n]{{{len(image) - len(monster[0]) + 1}}}".join(m.replace(" ", ".") for m in monster)

for t in transform(image):
    strings = ["".join(map(lambda b: '#' if b else '.', r)) for r in t]
    if n_monsters := len(re.findall(monster_pattern, "\n".join(strings), overlapped=True)):
        break

sol2 = np.count_nonzero(image) - n_monsters * sum(m.count("#") for m in monster)
print("Part Two: The number of '#'s that are not part of a sea monster is", sol2)
