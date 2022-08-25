"""
--- Day 1: Sonar Sweep ---
https://adventofcode.com/2020/day/1
"""
import aocd

DATA = [int(line) for line in aocd.data.splitlines()]

incs = sum(a < b for a, b in zip(DATA[:-1], DATA[1:]))
print("Part One:", incs)

incs = sum(sum(DATA[i: i + 3]) < sum(DATA[i + 1: i + 4]) for i in range(0, len(DATA) - 3))
print("Part Two:", incs)
