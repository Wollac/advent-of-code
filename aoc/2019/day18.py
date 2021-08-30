"""
--- Day 18: Many-Worlds Interpretation ---
https://adventofcode.com/2019/day/18
"""
from collections import defaultdict
from heapq import heappush, heappop

import aocd
import networkx as nx


def parse_graph(area):
    G = nx.Graph()
    for y, row in enumerate(area):
        for x, a in enumerate(row):
            if a == "#":
                continue
            if y > 0 and area[y - 1][x] != "#":
                G.add_edge((x, y - 1), (x, y), weight=1)
            if x > 0 and area[y][x - 1] != "#":
                G.add_edge((x - 1, y), (x, y), weight=1)

    # preprocess the graph
    modified = True
    while modified:
        modified = False

        # reduce all empty degree-2 nodes
        for node in list(G.nodes()):
            if G.degree(node) == 2 and area[node[1]][node[0]] == ".":
                e1, e2 = G.edges(node)
                weight = G[e1[0]][e1[1]]["weight"] + G[e2[0]][e2[1]]["weight"]
                if G.has_edge(e1[1], e2[1]):
                    G[e1[1]][e2[1]]["weight"] = min(G[e1[1]][e2[1]]["weight"], weight)
                else:
                    G.add_edge(e1[1], e2[1], weight=weight)
                G.remove_node(node)
                modified = True

        # remove all empty degree-1 nodes
        for node in list(G.nodes()):
            if G.degree(node) == 1 and area[node[1]][node[0]] == ".":
                G.remove_node(node)
                modified = True

    return G


def shortest(G: nx.Graph, sources: tuple):
    def cost(path):
        return sum(G[u][v]["weight"] for u, v in zip(path[:-1], path[1:]))

    dist = defaultdict(lambda: float("inf"), {(frozenset(), sources): 0})
    queue = []
    heappush(queue, (0, frozenset(), sources))
    while queue:
        length, collected, heads = heappop(queue)
        if len(collected) == len(keys):
            return length
        available = key_set - collected
        reachable = G.subgraph(G.nodes - door_set.difference(keys[k] for k in collected))
        for i, u in enumerate(heads):
            tree = nx.shortest_path(reachable, u, weight="weight")
            for v in available.intersection(tree.keys()):
                collected2 = collected | available.intersection(tree[v])
                length2 = length + cost(tree[v])
                targets = tuple(v if i == j else h for j, h in enumerate(heads))
                if length2 < dist[collected2, targets]:
                    dist[collected2, targets] = length2
                    heappush(queue, (length2, collected2, targets))


print(aocd.data)
grid = [list(line) for line in aocd.data.splitlines()]

sources = tuple((x, y) for y, row in enumerate(grid) for x, a in enumerate(row) if a == "@")
doors = {a.lower(): (x, y) for y, row in enumerate(grid) for x, a in enumerate(row) if a.isupper()}
door_set = set(doors.values())
keys = {(x, y): doors.get(a, None) for y, row in enumerate(grid) for x, a in enumerate(row) if a.islower()}
key_set = set(keys)

G = parse_graph(grid)
print(f"Graph: |N|={G.number_of_nodes()}, |E|={G.number_of_edges()}; Sources: {len(sources)}")
print("Part One:", shortest(G, sources))

source = sources[0]
for dx, dy in [(0, 0), (1, 0), (0, 1), (0, -1), (-1, 0)]:
    grid[source[1] + dy][source[0] + dx] = '#'
for dx, dy in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
    grid[source[1] + dy][source[0] + dx] = '@'
print("\n".join("".join(row) for row in grid))

sources = tuple((x, y) for y, row in enumerate(grid) for x, a in enumerate(row) if a == "@")

G = parse_graph(grid)
print(f"Graph: |N|={G.number_of_nodes()}, |E|={G.number_of_edges()}; Sources: {len(sources)}")
print("Part Two:", shortest(G, sources))
