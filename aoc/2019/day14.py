"""
--- Day 14: Space Stoichiometry ---
https://adventofcode.com/2019/day/14
"""
import bisect
import math
import re
from collections import Counter

import aocd

reactions = {product: (int(n), [(int(n), reactant) for n, reactant in re.findall(r"(\d+) ([A-Z]+)", reactants_raw)])
             for reactants_raw, n, product in re.findall(r"(.+) => (\d+) ([A-Z]+)", aocd.data)}


def get_ore(product: str, required: int, pool: Counter):
    # try to use from pool first
    if available := pool[product]:
        pool -= {product: required}  # this does not bring the count of the product below zero
        required -= available
    if required <= 0:
        return 0
    if product == "ORE":
        return required
    n, reactants = reactions[product]
    count = math.ceil(required / n)
    s = sum(get_ore(reactant, count * m, pool) for m, reactant in reactants)
    if excess := count * n - required:  # add potential excess product to the pool
        pool += {product: excess}
    return s


c = Counter()
print("Part One: The number of required 'ORE' to produce one 'FUEL' is", get_ore("FUEL", 1, c))
print("Produced excess products", c)


# dict with "compute if missing"
class ComputeDict(dict):
    def __init__(self, factory):
        super(ComputeDict, self).__init__()
        self.factory = factory

    def __missing__(self, key):
        self[key] = value = self.factory(key)
        return value


# do a binary search to find the first amount of FUEL that would require additional ORE
n_ore = 1000000000000
required_ore = ComputeDict(lambda x: get_ore("FUEL", x, Counter({"ORE": n_ore})))
print(f"Part Two: The amount of 'FUEL' that can be produced from {n_ore} 'ORE' is",
      bisect.bisect_right(required_ore, 0, 1, n_ore) - 1)
