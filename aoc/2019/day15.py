"""
--- Day 15: Oxygen System ---
https://adventofcode.com/2019/day/15
"""
import aocd
import networkx as nx

from .intcode import IntComputer

DIRS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
MOVES = {v: k for k, v in DIRS.items()}
PROGRAM = [int(n) for n in aocd.data.split(",")]


# move the droid one step, where m specifies the direction
def move_droid(droid, m):
    computer.input.append(m)
    n = (droid[0] + DIRS[m][0], droid[1] + DIRS[m][1])
    out = computer.run(until=IntComputer.op_output).popleft()
    if n in unexplored:
        unexplored.remove(n)
    if out == 0:
        area[n] = "#"
        G.remove_node(n)
        return droid
    if n not in area:
        area[n] = "o" if out == 2 else "."
        add_adjacent(n)
    return n


# adds all new reachable positions to the graph
def add_adjacent(pos):
    for d in DIRS.values():
        n = (pos[0] + d[0], pos[1] + d[1])
        if n not in area:
            G.add_edge(pos, n)
            unexplored.add(n)


# returns the moves required, to reach the nearest unexplored location
def explore_nearest(source):
    tree = nx.shortest_path(G, source)
    path = min((path for target, path in tree.items() if target in unexplored), key=lambda p: len(p))
    return [MOVES[(v[0] - u[0], v[1] - u[1])] for u, v in zip(path[:-1], path[1:])]


computer = IntComputer(PROGRAM)

droid = (0, 0)
area = {droid: "."}

unexplored = set()
G = nx.Graph()
G.add_node(droid)
add_adjacent(droid)

# explore the entire area
while unexplored:
    for move in explore_nearest(droid):
        droid = move_droid(droid, move)
oxygen_pos = next(pos for pos, v in area.items() if v == "o")

# draw the map
x_lo, x_hi = min(pos[0] for pos in area), max(pos[0] for pos in area)
y_lo, y_hi = min(pos[1] for pos in area), max(pos[1] for pos in area)
for y in range(y_lo, y_hi + 1):
    print("".join([area.get((x, y), " ") for x in range(x_lo, x_hi + 1)]))

print("Part One:", nx.shortest_path_length(G, (0, 0), oxygen_pos))
print("Part Two:", max(nx.shortest_path_length(G, oxygen_pos).values()))
