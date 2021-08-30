"""
--- Day 22: Slam Shuffle ---
https://adventofcode.com/2019/day/22
"""
import re

import aocd

DATA = aocd.data.splitlines()
nCards = 10007

techniques = {
    re.compile(r"deal into new stack"): lambda p: nCards - 1 - p,
    re.compile(r"cut (-?\d+)"): lambda p, n: (p - int(n)) % nCards,
    re.compile(r"deal with increment (\d+)"): lambda p, n: (p * int(n)) % nCards,
}

pos = 2019
for shuffle in DATA:
    for pattern, func in techniques.items():
        if m := re.fullmatch(pattern, shuffle):
            pos = func(pos, *m.groups())

print("Part One:", pos)

nCards = 119315717514047
nShuffles = 101741582076661

# First denotes the number of the first card in the deck.
# Increment denotes the difference between to consecutive numbers.
# The number of the card at a position p then corresponds to first + increment * p.
first, increment = 0, 1


def inv(n: int) -> int:
    """Computes the modular inverse of n."""
    # Fermat's little theorem states that n^(nCards - 1) ≡ 1 ⇒ 1/n ≡ n^(nCards - 2).
    return pow(n, nCards - 2, nCards)


def reverse(first, increment):
    increment *= -1  # reverse the order
    first += increment  # second number must become the fist
    return first % nCards, increment % nCards


def cut(first, increment, n):
    first += int(n) * increment  # move the n-th card to the front
    return first % nCards, increment


def spread(first, increment, n):
    # The card at the front does not change, the i-th card moves to position i*n.
    # This means that the increment (between the first and second card) is modified by i, where i * n ≡ 1.
    increment *= inv(int(n))
    return first, increment % nCards


techniques = {
    re.compile(r"deal into new stack"): reverse,
    re.compile(r"cut (-?\d+)"): cut,
    re.compile(r"deal with increment (\d+)"): spread,
}

for shuffle in DATA:
    for pattern, func in techniques.items():
        if m := re.fullmatch(pattern, shuffle):
            first, increment = func(first, increment, *m.groups())

# We now have the first and increment after one complete shuffle process.
# Applying another shuffle leads to:
#   first' = first + first * increment
#   increment' = increment * increment
# Thus, after n shuffles we get:
#   n=2: first + first * increment
#   n=3: first + first * increment + first * increment^2
#   n=4: first + first * increment + first * increment^2 + first * increment^3
#   ...
#   ∑ first * increment^k = first * (1 - increment^n)/(1 - increment)
#
# and for the increment:
#   increment^n

first = (first * (1 - pow(increment, nShuffles, nCards)) * inv(1 - increment)) % nCards
increment = pow(increment, nShuffles, nCards)

card = (first + 2020 * increment) % nCards
print("Part Two:", card)
