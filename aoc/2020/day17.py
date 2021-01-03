"""
--- Day 17: Conway Cubes ---
https://adventofcode.com/2020/day/17
"""
import aocd
import numpy as np

DATA = np.array([[c == '#' for c in line] for line in aocd.data.splitlines()])


def area(array, pos):
    indices = tuple(slice(max(p - 1, 0), p + 2) for p in pos)
    return array[indices]


def run(state, rounds):
    for _ in range(rounds):
        state = np.pad(state, (1, 1))
        tmp = state.copy()

        for pos in np.ndindex(state.shape):
            active = np.count_nonzero(area(state, pos))
            if state[pos]:
                if active != 3 and active != 4:
                    tmp[pos] = False
            else:
                if active == 3:
                    tmp[pos] = True

        state = tmp

    return state


# Part One

# make 3D
initial = DATA[np.newaxis, :]
n_rounds = 6
print(f"Part One: The number of active cubes after {n_rounds} rounds is", np.count_nonzero(run(initial, n_rounds)))

# Part Two

# make 4D
initial = DATA[np.newaxis, np.newaxis, :]
n_rounds = 6
print(f"Part Two: The number of active cubes after {n_rounds} rounds is", np.count_nonzero(run(initial, n_rounds)))
