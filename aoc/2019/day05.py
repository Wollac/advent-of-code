"""
--- Day 5: Sunny with a Chance of Asteroids ---
https://adventofcode.com/2019/day/5
"""
from collections import deque

import aocd

program = [int(n) for n in aocd.data.split(",")]


def get_value(mem, mode, param):
    if mode == "0":
        return mem[param]
    if mode == "1":
        return param
    raise RuntimeError(f"invalid read mode '{mode}'")


def set_value(mem, mode, param, v):
    if mode == "0":
        mem[param] = v
    else:
        raise RuntimeError(f"invalid write mode '{mode}'")


def run(mem: list, inputs: deque):
    output = deque()
    pc = 0
    while True:
        op = mem[pc] % 100
        modes = f"{mem[pc] // 100:03d}"[::-1]
        if op == 1:  # add
            params = mem[pc + 1: pc + 4]
            pc += 4
            v = get_value(mem, modes[0], params[0]) + get_value(mem, modes[1], params[1])
            set_value(mem, modes[2], params[2], v)
        elif op == 2:  # multiply
            params = mem[pc + 1: pc + 4]
            pc += 4
            v = get_value(mem, modes[0], params[0]) * get_value(mem, modes[1], params[1])
            set_value(mem, modes[2], params[2], v)
        elif op == 3:  # input
            params = mem[pc + 1: pc + 2]
            pc += 2
            set_value(mem, modes[0], params[0], inputs.popleft())
        elif op == 4:  # output
            params = mem[pc + 1: pc + 2]
            pc += 2
            output.append(get_value(mem, modes[0], params[0]))
        elif op == 5:  # jump-if-true
            params = mem[pc + 1: pc + 3]
            pc += 3
            if get_value(mem, modes[0], params[0]):
                pc = get_value(mem, modes[1], params[1])
        elif op == 6:  # jump-if-false
            params = mem[pc + 1: pc + 3]
            pc += 3
            if not get_value(mem, modes[0], params[0]):
                pc = get_value(mem, modes[1], params[1])
        elif op == 7:  # less-than
            params = mem[pc + 1: pc + 4]
            pc += 4
            v = get_value(mem, modes[0], params[0]) < get_value(mem, modes[1], params[1])
            set_value(mem, modes[2], params[2], v)
        elif op == 8:  # equal
            params = mem[pc + 1: pc + 4]
            pc += 4
            v = get_value(mem, modes[0], params[0]) == get_value(mem, modes[1], params[1])
            set_value(mem, modes[2], params[2], v)
        elif op == 99:  # return
            return output
        else:
            raise RuntimeError(f"invalid opcode '{op}'")


outputs = run(program.copy(), deque([1]))
print("Part One:", outputs.pop())

outputs = run(program.copy(), deque([5]))
print("Part Two:", outputs.pop())
