"""
--- Day 1: The Tyranny of the Rocket Equation ---
https://adventofcode.com/2019/day/1
"""
import aocd
import numpy as np

mass = np.array([int(n) for n in aocd.data.splitlines()])

fuel = mass // 3 - 2
print("Part One:", fuel.sum())

total = fuel
while not np.all(fuel == 0):
    fuel = np.where(fuel < 9, 0, fuel // 3 - 2)
    total += fuel
print("Part Two:", total.sum())
