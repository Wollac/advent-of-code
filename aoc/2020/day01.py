"""
--- Day 1: Report Repair ---
https://adventofcode.com/2020/day/1
"""
import aocd

DATA = set(int(line) for line in aocd.data.splitlines())


def find(s, n, inputs):
    if n == 1:
        return (s,) if s in inputs else None

    for i in inputs:
        rem = s - i
        if i >= rem / (n - 1):
            continue
        res = find(rem, n - 1, inputs)
        if res:
            return i, *res
    return None


# Part One

a, b = find(2020, 2, DATA)
print("Part One: %d * %d = %d" % (a, b, a * b))

# Part Two

a, b, c = find(2020, 3, DATA)
print("Part Two: %d * %d * %d = %d" % (a, b, c, a * b * c))
