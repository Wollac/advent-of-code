"""
--- Day 15: Rambunctious Recitation ---
https://adventofcode.com/2020/day/15
"""
import aocd

DATA = [int(x) for x in aocd.data.split(",")]


def game(starting, n):
    num = {n: t for t, n in enumerate(starting, 1)}
    last = starting[-1]
    for i in range(len(num), n):
        current = i - num.get(last, i)
        num[last] = i
        last = current
    return last


# Part One

n_turns = 2020
print(f"Part One: The {n_turns}th spoken number is", game(DATA, n_turns))

# Part Two

n_turns = 30000000
print(f"Part Two: The {n_turns}th spoken number is", game(DATA, n_turns))
