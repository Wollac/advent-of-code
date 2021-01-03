"""
--- Day 8: Handheld Halting ---
https://adventofcode.com/2020/day/8
"""
import re

import aocd

pattern = re.compile(r"(acc|jmp|nop) ([+-]?\d+)$")

program = []
for line in aocd.data.splitlines():
    m = re.match(pattern, line)
    if not m:
        raise ValueError("invalid entry '%s'" % line.strip())
    program.append((m[1], int(m[2])))


def run_program(program):
    visited = [False] * len(program)
    pc, acc = 0, 0
    while True:
        if pc == len(program):
            return acc

        if pc > len(program):
            raise RuntimeError("Invalid PC: %d" % pc, pc, acc)
        if visited[pc]:
            raise RuntimeError("Infinite loop at PC=%d ACC=%d" % (pc, acc), pc, acc)

        visited[pc] = True
        op, arg = program[pc]
        if op == "acc":
            acc += arg
            pc += 1
        elif op == "jmp":
            pc += arg
        elif op == "nop":
            pc += 1


# Part One

try:
    run_program(program)
except RuntimeError as err:
    msg, pc, acc = err.args
    print("Failed to run program: %s" % msg)
    print("Part One: The value in the accumulator before the error is %d" % acc)

# Part Two

for i, (op, arg) in enumerate(program):
    if op == "jmp":
        program[i] = ("nop", arg)
    elif op == "nop":
        program[i] = ("jmp", arg)
    else:
        continue
    try:
        v = run_program(program)
        print("Replacing '%s' in line %d with '%s' results in: %d" % (op, i, program[i][0], v))
        print("Part Two: The value of the accumulator after the program terminates is %d" % v)
        break
    except RuntimeError:
        program[i] = (op, arg)
