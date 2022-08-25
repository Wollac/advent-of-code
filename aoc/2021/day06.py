"""
--- Day 6: Lanternfish ---
https://adventofcode.com/2021/day/6
"""
from collections import Counter

import aocd
import numpy as np

DATA = np.fromstring(aocd.data, dtype=int, sep=',')

# use the brute-force method and compute age arrays as in the example
fish = np.copy(DATA)
for day in range(80):
    parent = (fish == 0)  # every fish with timer 0 creates a new fish
    fish -= 1  # decrease each timer
    fish[parent] = 6  # reset the timer of parents to 6
    fish = np.append(fish, np.full(np.count_nonzero(parent), 8))  # create the corresponding number of new fish

print("Part One", len(fish))

# for part two this method, obviously, gets out of hand
# so, we count the fish of each age values instead
ages = Counter(DATA)
for day in range(256):
    parents = ages[0]  # every fish with timer 0 creates a new fish
    for age in range(8):  # decrease each timer
        ages[age] = ages[age + 1]
    ages[6] += parents  # reset the timer of parents to 6
    ages[8] = parents  # create the corresponding number of new fish

print("Part Two", sum(ages.values()))
