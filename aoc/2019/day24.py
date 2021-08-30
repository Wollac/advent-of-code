"""
--- Day 24: Planet of Discord ---
https://adventofcode.com/2019/day/24
"""
from functools import reduce

import aocd
import numpy as np
from scipy import signal

DATA = np.array([[c == '#' for c in line] for line in aocd.data.splitlines()], dtype=int)


def biodiversity_rating(m: np.array) -> int:
    return reduce(lambda value, element: (value << 1) | element, m.flatten()[::-1])


def part_a() -> int:
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])  # 2d-adjacent cells
    matrix = DATA
    seen = set()
    while True:
        neighbors = signal.convolve2d(matrix, kernel, mode='same')
        matrix = (
                (matrix & (neighbors == 1)) |  # a bug dies unless there is exactly one bug adjacent
                # an empty space becomes a bug if exactly one or two bugs are adjacent
                (~matrix & ((neighbors == 2) | (neighbors == 1)))
        )
        rating = biodiversity_rating(matrix)
        # the rating is a bijection
        if rating in seen:
            return rating
        seen.add(rating)


print("Part One:", part_a())


def part_b(steps: int) -> int:
    kernel = np.array([
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ])
    tensor = np.pad(DATA[np.newaxis, :, :], [((steps + 1) // 2,), (0,), (0,)])

    for _ in range(steps):
        # count neighbors in the same level
        neighbors = signal.convolve(tensor, kernel, mode="same")

        # set all holes to zero
        neighbors[:, 2, 2] = 0

        # recurse down
        neighbors[0:-1, 0, :] += tensor[1:, 1, 2].reshape(-1, 1)  # top row += cell above hole next level
        neighbors[0:-1, :, 0] += tensor[1:, 2, 1].reshape(-1, 1)  # left column += cells left of hole next level
        neighbors[0:-1, :, -1] += tensor[1:, 2, 3].reshape(-1, 1)  # right column += cells right of hole next level
        neighbors[0:-1, -1, :] += tensor[1:, 3, 2].reshape(-1, 1)  # bottom row += cell below hole next level

        # recurse up
        neighbors[1:, 1, 2] += tensor[0:-1, 0, :].sum(axis=1)  # cell above hole += top row previous level
        neighbors[1:, 2, 1] += tensor[0:-1, :, 0].sum(axis=1)  # cell left of hole += left column previous level
        neighbors[1:, 2, 3] += tensor[0:-1, :, -1].sum(axis=1)  # cell right of hole += right column previous level
        neighbors[1:, 3, 2] += tensor[0:-1, -1, :].sum(axis=1)  # cell below of hole += bottom row previous level

        # next step is the same as part 1:
        tensor = ((tensor & (neighbors == 1)) | (~tensor & ((neighbors == 2) | (neighbors == 1))))

    return np.count_nonzero(tensor)


print("Part Two:", part_b(200))
