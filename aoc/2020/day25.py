"""
--- Day 25: Combo Breaker ---
https://adventofcode.com/2020/day/25
"""
import aocd

PUB = [int(n) for n in aocd.data.splitlines()]


# Part One

def ipow(b, exp):
    v = 1
    for _ in range(exp):
        v = (v * b) % 20201227
    return v


def ilog(b, a):
    v = 1
    x = 0
    while v != a:
        x += 1
        v = (v * b) % 20201227
    return x


priv = [ilog(7, key) for key in PUB]
print("Part One: The encryption key is", ipow(PUB[1], priv[0]))
