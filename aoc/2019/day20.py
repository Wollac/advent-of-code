"""
--- Day 20: Donut Maze ---
https://adventofcode.com/2019/day/20
"""
from collections import defaultdict
from heapq import heappush, heappop
from itertools import chain

import aocd
import networkx as nx


def parse_graph(data):
    G = nx.Graph()
    for y, row in enumerate(data):
        for x, a in enumerate(row):
            if a != ".":
                continue
            if y > 0 and data[y - 1][x] == ".":
                G.add_edge((x, y - 1), (x, y))
            if x > 0 and data[y][x - 1] == ".":
                G.add_edge((x - 1, y), (x, y))
    return G


def label(x, y, data):
    if data[y + 0][x - 1].isupper():
        return data[y][x - 2] + data[y][x - 1]
    if data[y + 0][x + 1].isupper():
        return data[y][x + 1] + data[y][x + 2]
    if data[y - 1][x + 0].isupper():
        return data[y - 2][x] + data[y - 1][x]
    if data[y + 1][x + 0].isupper():
        return data[y + 1][x] + data[y + 2][x]


def is_inner(x, y, data):
    return 3 <= y < len(data) - 3 and 3 <= x < len(data[y]) - 3


print(aocd.data)
grid = [list(line) for line in aocd.data.splitlines()]

G = parse_graph(grid)
inner = {l: (x, y) for y, row in enumerate(grid) for x, a in enumerate(row)
         if a == '.' and is_inner(x, y, grid) and (l := label(x, y, grid))}
outer = {l: (x, y) for y, row in enumerate(grid) for x, a in enumerate(row)
         if a == '.' and not is_inner(x, y, grid) and (l := label(x, y, grid))}

# create the directed graph induced by the labels
D = nx.DiGraph()
D.add_nodes_from(chain(inner.values(), outer.values()))
for n in D.nodes():
    tree = nx.shortest_path_length(G, n)
    for v in D.nodes():
        if n != v and v in tree:
            D.add_edge(n, v, weight=tree[v], level=0)
# add recursion edges
for n, n_coord in outer.items():
    if n in inner:  # outer -> inner: decrease level
        D.add_edge(n_coord, inner[n], weight=1, level=-1)
for n, n_coord in inner.items():
    if n in outer:  # inner -> outer: increase level
        D.add_edge(n_coord, outer[n], weight=1, level=1)

print(f"Labels: |inner|={len(inner)}, |outer|={len(outer)}; "
      f"Graph: |N|={D.number_of_nodes()}, |E|={D.number_of_edges()}")
# ignore the recursion for part one
print("Part One:", nx.dijkstra_path_length(D, outer["AA"], outer["ZZ"]))


def dijkstra_path_length(G, source, target):
    dist = defaultdict(lambda: float('inf'), {(source, 0): 0})
    queue = []
    heappush(queue, (0, source, 0))
    while queue:
        length, u, u_level = heappop(queue)
        if u == target and u_level == 0:
            return length
        for v, eattr in G[u].items():
            v_level = u_level + eattr["level"]
            if v_level < 0:
                continue
            alt = length + eattr["weight"]
            if alt < dist[v, v_level]:
                dist[v, v_level] = alt
                heappush(queue, (alt, v, v_level))


print("Part Two:", dijkstra_path_length(D, outer["AA"], outer["ZZ"]))
