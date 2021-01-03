"""
--- Day 5: Binary Boarding ---
https://adventofcode.com/2020/day/5
"""
import re

import aocd

pattern = re.compile(r"^([FB]{7})([LR]{3})$")

ids = set()
for line in aocd.data.splitlines():
    m = re.match(pattern, line)
    if not m:
        raise ValueError("invalid entry '%s'" % line.strip())
    row = 0
    for c in m[1]:
        row = row << 1
        if c == "B":
            row = row | 1
    column = 0
    for c in m[2]:
        column = column << 1
        if c == "R":
            column = column | 1
    seat_id = row * 8 + column
    ids.add(seat_id)

# Part One

print("Part One: The highest seat ID is %d" % max(ids))

# Part Two

missing, = set(range(min(ids), max(ids))) - ids
print("Part Two: The missing seat ID is %s" % missing)
