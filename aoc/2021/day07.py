"""
--- Day 7: The Treachery of Whales ---
https://adventofcode.com/2021/day/7
"""
import aocd
import numpy as np

DATA = np.fromstring(aocd.data, dtype=int, sep=',')

# the consumed fuel equals the distance between the start and x
print("Part One", min(np.abs(DATA - x).sum() for x in range(np.min(DATA), np.max(DATA) + 1)))


# Part Two
# the consumed fuel for distance n equals ∑ⁿk = ½·n(n+1)
def fuel(x):
    n = np.abs(DATA - x)
    return (n * (n + 1)) // 2


print("Part Two", min(fuel(x).sum() for x in range(np.min(DATA), np.max(DATA) + 1)))
