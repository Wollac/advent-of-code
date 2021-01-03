"""
--- Day 21: Allergen Assessment ---
https://adventofcode.com/2020/day/21
"""
import re

import aocd

DATA = [(set(foods.split()), set(algs.split(", "))) for foods, algs in re.findall(r"(.*) \(contains (.*)\)", aocd.data)]
FOODS = set.union(*(f for f, _ in DATA))
ALLERGENS = set.union(*(a for _, a in DATA))


# Part One

def bt(known):
    rem = {}
    for foods, algs in DATA:
        rem_algs = algs.difference(known[f] for f in foods if f in known)
        if not rem_algs.isdisjoint(known.values()):
            return False
        # extract foods with one remaining allergen
        if len(rem_algs) == 1:
            rem[rem_algs.pop()] = [f for f in foods if f not in known]
    if not rem:
        if ALLERGENS.issubset(known.values()):
            return True
        raise Exception("could not solve")

    # find the allergen with the least number of possible foods
    alg, foods = min(rem.items(), key=lambda item: len(item[1]))
    for food in foods:
        known[food] = alg
        if bt(known):
            return True
        del known[food]
    return False


impossibles = [f for f in FOODS if not any(bt({f: alg}) for alg in ALLERGENS)]
sol1 = sum((impossible in foods) for foods, _ in DATA for impossible in impossibles)
print("Part One: The number of times ingredients which cannot contain any allergens occur is", sol1)

# Part Two

assigned = {}
bt(assigned)

sol2 = ",".join(f for f, _ in sorted(assigned.items(), key=lambda item: item[1]))
print("Part Two: The dangerous ingredient list is", sol2)
