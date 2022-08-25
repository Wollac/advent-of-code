"""
--- Day 17: Trick Shot ---
https://adventofcode.com/2021/day/17
"""
import aocd
from parse import search

x1, x2 = search("x={:d}..{:d}", aocd.data)
y1, y2 = search("y={:d}..{:d}", aocd.data)


def step(vx, vy):
    x, y = 0, 0
    max_y = y
    hit = False
    while True:
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1

        if (y < y1 and vy <= 0) or (x < x1 and vx <= 0) or (x > x2 and vx >= 0):
            break

        max_y = max(max_y, y)
        if x1 <= x <= x2 and y1 <= y <= y2:
            hit = True

    if hit:
        return max_y


results = []
for dy in range(min(0, y1), max(abs(x1), abs(x2)) + 1):
    for dx in range(min(0, x1), max(0, x2) + 1):
        if (max_y := step(dx, dy)) is not None:
            results.append(max_y)

print("Part One", max(results))
print("Part Two", len(results))
