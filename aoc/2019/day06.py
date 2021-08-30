"""
--- Day 6: Universal Orbit Map ---
https://adventofcode.com/2019/day/6
"""
import aocd
import networkx as nx

G = nx.Graph([tuple(line.split(")")) for line in aocd.data.splitlines()])

tree = nx.shortest_path_length(G, "COM")
print("Part One:", sum(tree.values()))

print("Part Two:", nx.shortest_path_length(G, "YOU", "SAN") - 2)
