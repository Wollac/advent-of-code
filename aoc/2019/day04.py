"""
--- Day 4: Secure Container ---
https://adventofcode.com/2019/day/4
"""
from collections import Counter

import aocd

lo, hi = (int(n) for n in aocd.data.strip().split("-"))


def valid1(n):
    # it is a six-digit number.
    if not (100_000 <= n <= 999_999):
        return False
    digits = str(n)
    # the digits never decrease
    if not all(digits[i - 1] <= digits[i] for i in range(1, len(digits))):
        return False
    # two adjacent digits are the same
    if not any(digits[i - 1] == digits[i] for i in range(1, len(digits))):
        return False
    return True


print("Part One:", sum(valid1(i) for i in range(lo, hi + 1)))


def valid2(n):
    # it is a six-digit number.
    if not (100_000 <= n <= 999_999):
        return False
    digits = str(n)
    # the digits never decrease
    if not all(digits[i - 1] <= digits[i] for i in range(1, len(digits))):
        return False
    # two adjacent digits are the same, but not part of a larger group of matching digits
    if 2 not in Counter(digits).values():  # as the digits never decrease this only counts adjacent duplicates
        return False
    return True


print("Part Two:", sum(valid2(i) for i in range(lo, hi + 1)))
