"""
--- Day 4: Giant Squid ---
https://adventofcode.com/2021/day/4
"""
import aocd
import numpy as np

numbers, *boards = aocd.data.splitlines()
numbers = map(int, numbers.split(','))
boards = np.loadtxt(boards, int).reshape((-1, 5, 5))  # all the boards are 5x5
print(f"There are {len(boards)} 5x5 boards with numbers from {np.min(boards)} to {np.max(boards)}.")

scores = []
for n in numbers:
    boards[boards == n] = -1  # set the drawn numbers to -1 to mark them

    m = (boards == -1)  # get marked fields of all boards
    # get the indices of all the boards that have a complete row or complete column marked
    indices = (m.all(1) | m.all(2)).any(1)
    for i in np.argwhere(indices):  # compute scores for all those board indices
        scores.append(n * np.sum(boards[i], where=(boards[i] != -1)))  # sum of all unmarked numbers times n
    boards = boards[~indices]  # only keep the non-winning boards

    # we can stop, if there are no more boards left
    if len(boards) == 0:
        break

print("Part One", scores[0])
print("Part Two", scores[-1])
