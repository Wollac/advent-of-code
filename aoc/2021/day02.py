"""
--- Day 2: Dive! ---
https://adventofcode.com/2021/day/2
"""
import aocd

DATA = [line.split() for line in aocd.data.splitlines()]
print(DATA)

pos, depth = 0, 0
for data, n in DATA:
    if data == "forward":
        pos += int(n)
    elif data == "up":
        depth -= int(n)
    elif data == "down":
        depth += int(n)

print("Part One:", pos * depth)

pos, depth, aim = 0, 0, 0
for data, n in DATA:
    if data == "forward":
        pos += int(n)
        depth += aim * int(n)
    elif data == "up":
        aim -= int(n)
    elif data == "down":
        aim += int(n)

print("Part Two:", pos * depth)
