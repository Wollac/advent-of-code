"""
--- Day 17: Set and Forget ---
https://adventofcode.com/2019/day/17
"""
from typing import List

import aocd
import networkx as nx

from .intcode import IntComputer

FUNCTIONS = "ABC"  # feasible function names
PROGRAM = [int(n) for n in aocd.data.split(",")]

output = "".join(chr(c) for c in IntComputer(PROGRAM).run())
area = output.splitlines()

G = nx.Graph()
for y, row in enumerate(area):
    for x, a in enumerate(row):
        if a == ".":
            continue
        if y > 0 and area[y - 1][x] != ".":
            G.add_edge((x, y - 1), (x, y))
        if x > 0 and area[y][x - 1] != ".":
            G.add_edge((x - 1, y), (x, y))

print("Part One:", sum(n[0] * n[1] for n in G.nodes() if G.degree(n) > 2))


def right(direction):
    return -direction[1], direction[0]


def left(direction):
    return direction[1], -direction[0]


# Returns the movements along the Eulerian path starting in source
def move(source, heading):
    res = []
    forward = 0
    u = source
    while True:
        if G.has_edge(u, (u[0] + heading[0], u[1] + heading[1])):
            forward += 1
        elif G.has_edge(u, (u[0] + right(heading)[0], u[1] + right(heading)[1])):
            res += [str(forward), "R"]
            heading = right(heading)
            forward = 1
        elif G.has_edge(u, (u[0] + left(heading)[0], u[1] + left(heading)[1])):
            res += [str(forward), "L"]
            heading = left(heading)
            forward = 1
        else:
            break  # we have reached a node with degree 1
        u = (u[0] + heading[0], u[1] + heading[1])
    if forward:
        res.append(str(forward))
    return res


robot = next((x, y) for (x, y) in G.nodes if area[y][x] in "^v<>")
if G.degree(robot) != 1:
    raise ValueError("robot must start on a deg-1 node")

heading = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}[area[robot[1]][robot[0]]]
moves = move(robot, heading)[1:]  # ignore the leading '0'
move_str = ",".join(moves) + ","


# generator for all feasible compressions of the given string
def compressions(string: str, chunks=[], length=0):
    if len(chunks) > len(FUNCTIONS) or length > 21 // 2:
        return
    if string == "":
        yield chunks
    # try all possible next chunks
    for stop in range(1, min(21, len(string))):
        chunk = string[:stop]
        if "\0" in chunk or chunk[-1] != ",":
            continue
        # replace all occurrences of chunk and try to compress further
        yield from compressions(string.replace(chunk, "\0").strip("\0"), chunks + [chunk], length + string.count(chunk))


def compress(string: str, chunks: List[str]):
    for i, chunk in enumerate(chunks):
        string = string.replace(chunk, FUNCTIONS[i])
    return [",".join(list(string))] + [chunk.rstrip(",") for chunk in chunks]  # separated by ',' but no trailing ','s


# find the best compression
inputs = min((compress(move_str, chunks) for chunks in compressions(move_str)), key=lambda input: len("\n".join(input)))
input_str = "\n".join(inputs) + "\nn\n"  # 'n' for no continuous video feed
print("Input:\n" + input_str)

*output, amount = IntComputer([2] + PROGRAM[1:], inputs=(ord(c) for c in input_str)).run()
print("Output:\n" + "".join([chr(c) for c in output]))
print("Part Two:", amount)
