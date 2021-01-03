"""
--- Day 23: Crab Cups ---
https://adventofcode.com/2020/day/23
"""
from collections import deque

import aocd

DATA = [int(c) for c in aocd.data.strip()]


# Part One

def game(cups, rounds):
    d = deque(cups)
    n = len(cups)
    for _ in range(rounds):
        current = d[0]
        d.rotate(-1)
        pick = [d.popleft() for _ in range(3)]

        dst = current - 1 or n
        while dst in pick:
            dst = dst - 1 or n

        dist = d.index(dst)
        d.rotate(-1 - dist)

        d.extend(pick)
        d.rotate(4 + dist)

    return d


cups = game(DATA, 100)

cups.rotate(-1 - cups.index(1))
sol1 = "".join(str(cups.popleft()) for _ in range(len(cups) - 1))
print("Part One: The labels on the cups after cup '1' are", sol1)


# Part Two

class Cup:
    __slots__ = "label", "next"

    def __init__(self, label):
        self.label = label
        self.next = None
        nodes[label] = self


def game2(cups, rounds):
    head = tail = Cup(cups[0])
    for cup in cups[1:]:
        tail.next = tail = Cup(cup)
    tail.next = head  # make a ring

    n = len(cups)
    for _ in range(rounds):
        pick = head.next
        head.next = pick.next.next.next

        label = head.label - 1 or n
        while label in [pick.label, pick.next.label, pick.next.next.label]:
            label = label - 1 or n

        dst = nodes[label]
        pick.next.next.next = dst.next
        dst.next = pick

        head = head.next

    one = nodes[1]
    return [one.label, one.next.label, one.next.next.label]


nodes = {}
cups = game2([DATA[i] if i < len(DATA) else i + 1 for i in range(1000000)], 10000000)
print(f"Part Two: The product of the two cups after cup '1' is {cups[1]} * {cups[2]} = {cups[1] * cups[2]}")
