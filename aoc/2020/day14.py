"""
--- Day 14: Docking Data ---
https://adventofcode.com/2020/day/14
"""
import re

import aocd

mask_pattern = re.compile(r"mask = ([X01]{36})$")
mem_pattern = re.compile(r"mem\[(\d+)\] = (\d+)$")

program = []
for line in aocd.data.splitlines():
    if line.startswith("mask"):
        m = re.match(mask_pattern, line)
        program.append(("mask", m[1]))
    elif line.startswith("mem"):
        m = re.match(mem_pattern, line)
        program.append(("mem", (int(m[1]), int(m[2]))))

# Part One

mask = (0, ~0)
mem = {}
for op, args in program:
    if op == "mask":
        or_mask, and_mask = 0, 0
        for i, c in enumerate(args[::-1]):
            if c == '0':
                and_mask |= 1 << i
            elif c == '1':
                or_mask |= 1 << i
        mask = (or_mask, ~and_mask)
    elif op == "mem":
        mem[args[0]] = (args[1] | mask[0]) & mask[1]

print("Part One: The sum of all memory values is", sum(mem.values()))


# Part Two

def memset(mask, addr, v):
    i = mask.find('X')
    if i >= 0:
        m = mask[:i] + '0' + mask[i + 1:]
        memset(m, addr & ~(1 << i), v)
        memset(m, addr | (1 << i), v)
        return

    for i, b in enumerate(mask):
        if b == '1':
            addr |= 1 << i
    mem[addr] = v


mask = '0' * 36
mem = {}
for op, args in program:
    if op == "mask":
        mask = args[::-1]
    elif op == "mem":
        memset(mask, args[0], args[1])

print("Part Two: The sum of all memory values is", sum(mem.values()))
