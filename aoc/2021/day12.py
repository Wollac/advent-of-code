"""
--- Day 12: Passage Pathing ---
https://adventofcode.com/2021/day/12
Start: 05:26 Part 1: 05:44 Part 2: 05:47
"""
from collections import defaultdict

import aocd

DATA = [line.split('-') for line in aocd.data.splitlines()]

# construct the corresponding graph as an adjacency list
G = defaultdict(list)
for u, v in DATA:
    G[u].append(v)
    G[v].append(u)

# DFS to enumerate all the valid paths
count = 0
S = [["start"]]
while S:
    path = S.pop()
    for v in G[path[-1]]:
        if v == "end":
            count += 1
            continue
        # valid paths visit small caves at most once and can visit big caves any number of times
        if v.islower() and v in path:
            continue
        S.append(path + [v])

print("Part One", count)

# DFS to enumerate all the valid paths
count = 0
S = [(["start"], False)]  # an element consists of the path and whether it contains a small cave twice
while S:
    path, dup = S.pop()
    for v in G[path[-1]]:
        if v == "end":
            count += 1
            continue
        if v == "start":
            continue
        # valid paths visit at most one small cave twice and can visit big caves any number of times
        if v.islower() and v in path:
            if dup:  # the path already contains a small cave twice
                continue
            S.append((path + [v], True))
        else:
            S.append((path + [v], dup))

print("Part Two", count)
