"""
--- Day 20: Trench Map ---
https://adventofcode.com/2021/day/20
Start: 01:25 Part 1: 01:27 Part 2: 01:56
"""
from collections import Counter, namedtuple

import aocd
import parse

DATA = []
for _, p in parse.findall("Player {:d} starting position: {:d}", aocd.data):
    DATA.append(p - 1)  # we denote the fields 0-9 instead of 1-10
print(aocd.data)


class Die:
    """Simple deterministic die"""

    def __init__(self, sides):
        self.rolls = 0
        self._sides = sides

    def __next__(self):
        result = self.rolls % self._sides + 1
        self.rolls += 1
        return result


def deterministic(pos: list[int], target=1000) -> int:
    die = Die(100)  # 100-sided die

    n = len(pos)
    score = [0] * n
    while True:
        for i in range(n):
            for _ in range(3):  # roll three times
                roll = next(die)
                pos[i] = (pos[i] + roll) % 10

            score[i] += pos[i] + 1
            if score[i] >= target:
                return score[(i + 1) % n] * die.rolls


print("Part One", deterministic(DATA.copy()))

# Part Two
# We explore the entire state-space. A state consists of (a) the active player, (b) the positions, (c) the scores.
# However, the same state can be reached in multiple "universes". As such, we need to count occurrences of each state.
# The max number of distinct states is 2*10*10*21*21, which is feasible to explore.

State = namedtuple("State", ["player", "positions", "scores"])

# precompute all possible results of the dice roll together with their probability
ROLLS = Counter(a + b + c for a in range(1, 4) for b in range(1, 4) for c in range(1, 4))


def quantum(start: list[int], target=21):
    n = len(start)
    initial = State(0, tuple(start), (0,) * n)
    states = Counter((initial,))

    results = [0] * n
    while states:
        for state, state_count in states.copy().items():
            del states[state]

            i = state.player
            pos, score = list(state.positions), list(state.scores)
            for roll, count in ROLLS.items():
                pos[i] = (state.positions[i] + roll) % 10
                score[i] = state.scores[i] + pos[i] + 1
                if score[i] >= target:
                    results[i] += state_count * count
                else:
                    states[State((i + 1) % n, tuple(pos), tuple(score))] += state_count * count

    return results


winning = quantum(DATA)
print(f"Player 1 wins with a probability of {winning[0] / sum(winning):%}.")
print("Part Two", max(winning))
