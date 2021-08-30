"""
--- Day 8: Space Image Format ---
https://adventofcode.com/2019/day/8
"""
from functools import reduce

import aocd
import numpy as np

a = np.array([int(c) for c in aocd.data.strip()]).reshape(-1, 6, 25)

max_layer = max(a, key=np.count_nonzero)
print("Part One:", np.count_nonzero(max_layer == 1) * np.count_nonzero(max_layer == 2))

image = reduce(lambda x, y: np.where(x == 2, y, x), a)
for row in np.where(image == 1, "█", " "):
    print("".join(row))
