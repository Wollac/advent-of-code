"""
--- Day 13: Shuttle Search ---
https://adventofcode.com/2020/day/13
"""
import re
from itertools import count
from math import ceil

import aocd

first, table = aocd.data.splitlines()
arrival = int(first)
busses = {int(n): i for i, n in enumerate(re.findall(r"\d+|x", table)) if n != "x"}

# Part One

departure, bus = min((ceil(arrival / n) * n, n) for n in busses.keys())
wait = departure - arrival
print(f"Part One: Earliest bus ID {bus} departing after {wait} minutes {bus} * {wait} = {bus * wait}")


# Part Two

def solve():
    start, step = 0, 1
    for n, offset in busses.items():
        for ts in count(start, step):
            if (ts + offset) % n == 0:
                start = ts
                step *= n
                break
    return start


print("Part Two: The earliest feasible timestamp is", solve())
