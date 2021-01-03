"""
--- Day 7: Handy Haversacks ---
https://adventofcode.com/2020/day/7
"""
import re
from collections import defaultdict

import aocd

outer_pattern = re.compile(r"([a-z ]+) bags contain")
inner_pattern = re.compile(r"(\d+) ([a-z ]+) bags?[,.]")

DATA = {}
for line in aocd.data.splitlines():
    m = re.match(outer_pattern, line)
    if not m:
        raise ValueError("invalid entry '%s'" % line.strip())
    outer = m[1]
    inners = []
    for m in re.finditer(inner_pattern, line):
        inners.append((int(m[1]), m[2]))
    if outer in DATA:
        raise ValueError("outer bag '%s' already defined" % outer)
    DATA[outer] = inners

# invert the bag relation dict
inv = defaultdict(list)
for outer, inners in DATA.items():
    for _, bag in inners:
        inv[bag].append(outer)


# Part One

def count_outers(bag):
    outers = {bag}

    done = False
    while not done:
        done = True
        for inner in outers.copy():
            for outer in inv[inner]:
                if outer not in outers:
                    outers.add(outer)
                    done = False

    outers.remove(bag)
    return len(outers)


print("Part One: The number of bags that can contain a 'shiny gold' bag is %d" % count_outers("shiny gold"))


# Part Two

def count_inners(bag):
    result = 0
    for count, inner in DATA[bag]:
        result += count + count * count_inners(inner)
    return result


print("Part Two: The number of bags required inside a 'shiny gold' bag is %d" % count_inners("shiny gold"))
