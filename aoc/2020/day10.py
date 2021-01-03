"""
--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10
"""
import aocd

DATA = {int(n) for n in aocd.data.splitlines()}
OUTPUT = max(DATA) + 3
DATA.add(OUTPUT)

# Part One

adapter_chain = [0]
while len(adapter_chain) <= len(DATA):
    for a in range(1, 4):
        c = adapter_chain[-1] + a
        if c in DATA:
            adapter_chain.append(c)
            break
    else:
        raise Exception("Invalid input")


def countdelta(chain, d):
    result = 0
    last = chain[0]
    for c in chain[1:]:
        if c - last == d:
            result += 1
        last = c
    return result


a, b = countdelta(adapter_chain, 1), countdelta(adapter_chain, 3)
print("Part One: The number of 1-differences multiplied by the number of 3-differences is %d * %d = %d" % (a, b, a * b))


# Part Two

def count(adapters, i, o):
    if i > o:
        return 0
    if i == o:
        return 1
    if i in cache:
        return cache[i]

    res = 0
    for a in range(1, 4):
        c = i + a
        if c in adapters:
            adapters.remove(c)
            res += count(adapters, c, o)
            adapters.add(c)

    cache[i] = res
    return res


cache = {}
sol2 = count(DATA.copy(), 0, OUTPUT)
print("Part Two: The total number of distinct ways it connect the adapters is %d" % sol2)
