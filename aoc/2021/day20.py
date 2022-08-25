"""
--- Day 20: Trench Map ---
https://adventofcode.com/2021/day/20
Start: 12:27 Part 1: 13:08 Part 2: 13:10
"""
import aocd
import numpy as np
from scipy import ndimage

algo, image = aocd.data.split("\n\n")
algo = np.array([int(p == "#") for p in algo])
image = np.array([[int(c == "#") for c in row] for row in image.splitlines()])
assert len(algo) == 1 << 9

# weights to convert binary numbers
weights = np.array(
    [[1 << 0, 1 << 1, 1 << 2],
     [1 << 3, 1 << 4, 1 << 5],
     [1 << 6, 1 << 7, 1 << 8]]
)


def enhance(a: np.ndarray, n: int) -> np.ndarray:
    a = np.pad(a, n)  # extend by n pixel in all four directions
    for _ in range(n):
        a = algo[ndimage.convolve(a, weights, mode="nearest")]  # the pixels at infinity must match the nearest
    return a


print("Part One", np.count_nonzero(enhance(image, 2)))
print("Part Two", np.count_nonzero(enhance(image, 50)))
