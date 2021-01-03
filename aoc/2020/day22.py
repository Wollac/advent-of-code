"""
--- Day 22: Crab Combat ---
https://adventofcode.com/2020/day/22
"""
import re
from collections import deque
from itertools import islice

import aocd

DATA = {int(n): [int(c) for c in cards_raw.splitlines()]
        for n, cards_raw, _ in re.findall(r"Player (\d+):\n((\d+\n?)+)", aocd.data)}


# Part One

def game1(decks):
    while all(deck for deck in decks):
        play = [deck.popleft() for deck in decks]
        winner = play.index(max(play))
        decks[winner].extend(sorted(play, reverse=True))


def score(deck):
    return sum(i * card for i, card in enumerate(reversed(deck), 1))


cards = [deque(DATA[n]) for n in sorted(DATA.keys())]
game1(cards)

winning = max(cards, key=lambda deck: len(deck))
print("Part One: The winning player's score is", score(winning))


# Part Two

def game2(deck1, deck2):
    seen = set()
    while deck1 and deck2:
        key = (tuple(deck1), tuple(deck2))
        if key in seen:
            return 1
        seen.add(key)

        play1, play2 = deck1.popleft(), deck2.popleft()
        if play1 <= len(deck1) and play2 <= len(deck2):
            winner = game2(
                deque(islice(deck1, play1)),
                deque(islice(deck2, play2))
            )
        else:
            winner = 1 if play1 > play2 else 2

        if winner == 1:
            deck1 += (play1, play2)
        else:
            deck2 += (play2, play1)

    if not deck1:
        return 2
    return 1


cards = [deque(DATA[n]) for n in sorted(DATA.keys())]
game2(cards[0], cards[1])

winning = max(cards, key=lambda deck: len(deck))
print("Part Two: The winning player's score is", score(winning))
