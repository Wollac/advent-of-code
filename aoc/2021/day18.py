"""
--- Day 18: Snailfish ---
https://adventofcode.com/2021/day/18
"""
import ast
import copy
from functools import reduce

import aocd


class Number:
    __slots__ = "num", "left", "right"

    def __init__(self, num, left=None, right=None):
        assert num is not None or (left and right)
        self.num = num
        self.left = left
        self.right = right

    def __str__(self):
        if self.is_regular():
            return str(self.num)
        return "[" + str(self.left) + "," + str(self.right) + "]"

    def is_regular(self):
        return self.num is not None


def number(a) -> Number:
    if isinstance(a, int):
        return Number(a)
    return Number(None, number(a[0]), number(a[1]))


numbers = [number(ast.literal_eval(line)) for line in aocd.data.splitlines()]


def add_left(n: Number, v: int):
    if not n:
        return
    if n.is_regular():
        n.num += v
    else:
        add_left(n.left, v)


def add_right(n: Number, v: int):
    if not n:
        return
    if n.is_regular():
        n.num += v
    else:
        add_right(n.right, v)


def explode(n: Number, depth, left, right):
    if n.is_regular():
        return False
    # explode the first pair that is nested inside four pairs
    if depth == 4 and n.left.is_regular() and n.right.is_regular():
        add_right(left, n.left.num)  # add to the first regular number to the left
        add_left(right, n.right.num)  # add to the first regular number to the right
        # replace n with the regular number 0
        n.num = 0
        n.left = n.right = None
        return True

    return explode(n.left, depth + 1, left, n.right) or explode(n.right, depth + 1, n.left, right)


def split(n: Number):
    if not n.is_regular():
        return split(n.left) or split(n.right)
    # split the first regular number that is 10 or greater
    if n.num >= 10:
        n.left = Number(n.num // 2)
        n.right = Number((n.num + 1) // 2)
        n.num = None
        return True

    return False


def add(a: Number, b: Number) -> Number:
    result = Number(None, copy.deepcopy(a), copy.deepcopy(b))
    # reduce the result
    while explode(result, 0, None, None) or split(result):
        pass
    return result


def magnitude(n: Number) -> int:
    if n.is_regular():
        return n.num
    return 3 * magnitude(n.left) + 2 * magnitude(n.right)


s = reduce(add, numbers)
print(f"The sum of the {len(numbers)} numbers is: {s}")
print("Part One", magnitude(s))

print("Part Two", max(magnitude(add(n1, n2)) for n1 in numbers for n2 in numbers if n1 != n2))
