"""
--- Day 9: Encoding Error ---
https://adventofcode.com/2020/day/9
"""
from collections import deque

import aocd

DATA = [int(n) for n in aocd.data.splitlines()]


# Part One

def pairsum(preamble, v):
    for a in preamble:
        if a > v:
            continue
        for b in preamble:
            if a + b == v:
                return True
    return False


def first_invalid(numbers):
    q = deque(numbers[:25])
    for i in numbers[25:]:
        if not pairsum(q, i):
            return i
        q.popleft()
        q.append(i)


invalid = first_invalid(DATA)
print("Part One: The first invalid number is %d" % invalid)


# Part Two

def subsetsum(n, s):
    q = deque(DATA[:n])
    for i in DATA[n:]:
        if sum(q) == s:
            return q
        q.popleft()
        q.append(i)

    return None


for n in range(2, len(DATA)):
    if d := subsetsum(n, invalid):
        print("Part Two: The encryption weakness is %d + %d = %d" % (min(d), max(d), min(d) + max(d)))
        break
