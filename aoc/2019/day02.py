"""
--- Day 2: 1202 Program Alarm ---
https://adventofcode.com/2019/day/2
"""
import aocd

program = [int(n) for n in aocd.data.split(",")]


def run(mem, p1, p2):
    mem[1], mem[2] = p1, p2
    pc = 0
    while True:
        op = mem[pc]
        if op == 99:
            return mem[0]
        ax, bx, cx = mem[pc + 1: pc + 4]
        pc += 4
        if op == 1:
            mem[cx] = mem[ax] + mem[bx]
        elif op == 2:
            mem[cx] = mem[ax] * mem[bx]
        else:
            return None


sol1 = run(program.copy(), 12, 2)
print("Part One:", sol1)

a, b = next((a, b) for a in range(len(program)) for b in range(len(program)) if run(program.copy(), a, b) == 19690720)
print("Part Two:", 100 * a + b)
