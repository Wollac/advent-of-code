"""
--- Day 10: Syntax Scoring ---
https://adventofcode.com/2021/day/10
Start: 06:18 Part 1: 06:29 Part 2: 06:39
"""
import functools

import aocd

DATA = aocd.data.splitlines()
PAIRS = ["()", "[]", "{}", "<>"]

close2open = {c: o for o, c in PAIRS}

# Part One
POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}

p = []
for line in DATA:
    stack = []
    for c in line:
        if c not in close2open:  # opening
            stack.append(c)
        elif stack and stack[-1] == close2open[c]:  # valid close
            stack.pop()
        else:  # corrupted close
            p.append(POINTS[c])
            break

print("Part One", sum(p))

# Part Two
POINTS = {'(': 1, '[': 2, '{': 3, '<': 4}

p = []
for line in DATA:
    stack = []
    for c in line:
        if c not in close2open:  # opening
            stack.append(c)
        elif stack and stack[-1] == close2open[c]:  # valid close
            stack.pop()
        else:  # corrupted close
            break
    else:  # not corrupted but incomplete
        total = functools.reduce(lambda v, c: v * 5 + POINTS[c], reversed(stack), 0)
        p.append(total)

print("Part Two", sorted(p)[len(p) // 2])
