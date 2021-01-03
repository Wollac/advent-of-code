"""
--- Day 2: Password Philosophy ---
https://adventofcode.com/2020/day/2
"""
import re

import aocd

DATA = [re.match(r"(\d*)-(\d*) ([a-z]): ([a-z]*)", line).groups() for line in aocd.data.splitlines()]


def valid1(entry):
    x, y = int(entry[0]), int(entry[1])
    char = entry[2]
    passwd = entry[3]

    count = passwd.count(char)
    return True if x <= count <= y else False


def valid2(entry):
    x, y = int(entry[0]), int(entry[1])
    char = entry[2]
    passwd = entry[3]
    if x < 1 or len(passwd) < y:
        return False

    a, b = passwd[x - 1], passwd[y - 1]
    return True if (a == char) != (b == char) else False


count1 = sum(valid1(entry) for entry in DATA)
print("Part One: The number of valid passwords is %d" % count1)

count2 = sum(valid2(entry) for entry in DATA)
print("Part Two: The number of valid passwords is %d" % count2)
