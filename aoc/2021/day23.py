"""
--- Day 23: Amphipod ---
https://adventofcode.com/2021/day/23
"""
import itertools

import aocd
import networkx as nx

AREA = [list(line) for line in aocd.data.splitlines()]
COST = [1, 10, 100, 1000]


def all_shortest_paths(grid: list[list]) -> dict:
    G = nx.Graph()
    for y, row in enumerate(grid):
        for x, a in enumerate(row):
            if a == "#" or a == " ":
                continue
            if y > 0 and grid[y - 1][x] != "#":
                G.add_edge((x, y - 1), (x, y))
            if x > 0 and grid[y][x - 1] != "#":
                G.add_edge((x - 1, y), (x, y))
    return {(s, t): set(nx.shortest_path(G, s, t)) - {s} for s in G.nodes() for t in G.nodes()}


def parse(grid: list[list]) -> (list[tuple], list[list[tuple]], list[list]):
    top_coord = [(x, y) for y, row in enumerate(grid) for x, a in enumerate(row) if a == "." and grid[y + 1][x] == "#"]

    rooms_map = {(x, y): ord(a) - ord('A') for y, row in enumerate(grid) for x, a in enumerate(row) if a.isupper()}
    rooms_coord = [[k for k, _ in g] for _, g in itertools.groupby(sorted(rooms_map.items()), key=lambda k: k[0][0])]
    initial = [[v for _, v in g] for _, g in itertools.groupby(sorted(rooms_map.items()), key=lambda k: k[0][0])]

    return top_coord, rooms_coord, initial


def reachable(s, t, blocked: set):
    return blocked.isdisjoint(all_paths[(s, t)])


def dist(a: int, s: tuple, t: tuple):
    return len(all_paths[(s, t)]) * COST[a]


def room_in(i, room):
    for idx, r in reversed(list(enumerate(room))):
        if r is None:
            return idx
        if i != r:
            break
    return -1


def room_out(i, room):
    if all(r is None or r == i for r in room):
        return -1
    for idx, r in enumerate(room):
        if r is not None:
            return idx


def hash_key(top, rooms) -> int:
    k = 0
    for a in top:
        k = k * 5 + (4 if a is None else a)
    for room in rooms:
        for a in room:
            k = k * 5 + (4 if a is None else a)
    return k


def search(top: list, rooms: list[list]) -> int:
    if all(all(i == a for a in room) for i, room in enumerate(rooms)):
        return 0

    key = hash_key(top, rooms)
    if key in cache:
        return cache[key]

    blocked = set(top_coord[i] for i, a in enumerate(top) if a is not None)

    result = float("inf")
    for si, a in enumerate(top):
        if a is not None and (di := room_in(a, rooms[a])) >= 0:
            s, t = top_coord[si], rooms_coord[a][di]
            if reachable(s, t, blocked):
                new_top = top[:]
                new_top[si] = None
                new_rooms = [room[:] for room in rooms]
                new_rooms[a][di] = a
                result = dist(a, s, t) + search(new_top, new_rooms)
                break  # this is always optimal
    else:
        for i, room in enumerate(rooms):
            if (si := room_out(i, room)) >= 0:
                for di in (i for i, t in enumerate(top) if t is None):
                    s, t = rooms_coord[i][si], top_coord[di]
                    if reachable(s, t, blocked):
                        a = rooms[i][si]
                        new_top = top[:]
                        new_top[di] = a
                        new_rooms = [room[:] for room in rooms]
                        new_rooms[i][si] = None
                        result = min(result, dist(a, s, t) + search(new_top, new_rooms))

    cache[key] = result
    return result


print("\n".join("".join(row) for row in AREA))

top_coord, rooms_coord, initial = parse(AREA)
all_paths = all_shortest_paths(AREA)
cache = {}
print("Part One", search([None] * len(top_coord), initial))
print(f"Explored {len(cache)} states.")

AREA.insert(3, list("  #D#C#B#A#"))
AREA.insert(4, list("  #D#B#A#C#"))
print("\n".join("".join(row) for row in AREA))

top_coord, rooms_coord, initial = parse(AREA)
all_paths = all_shortest_paths(AREA)
cache = {}
print("Part Two", search([None] * len(top_coord), initial))
print(f"Explored {len(cache)} states.")
