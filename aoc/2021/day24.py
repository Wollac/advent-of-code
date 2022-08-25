"""
--- Day 24: Arithmetic Logic Unit ---
https://adventofcode.com/2021/day/24
"""
import re
import aocd

DATA = ["inp" + block for block in filter(None, aocd.data.split("inp"))]
DATA = [[tuple(line.split(" ")) for line in block.splitlines()] for block in DATA]
N = len(DATA)


def solve(instructions, var):
    for i, (opcode, *args) in reversed(list(enumerate(instructions))):
        if args[0] == var:
            if opcode == "inp":
                return "inp"

            left = solve(instructions[:i], var)
            if args[1].islower():
                right = solve(instructions[:i], args[1])
            else:
                right = args[1]

            if opcode == "add":
                if left == "0":
                    return right
                if right == "0":
                    return left
                return "(" + left + " + " + right + ")"
            elif opcode == "mul":
                if left == "1":
                    return right
                if right == "1":
                    return left
                if left == "0" or right == "0":
                    return "0"
                return "(" + left + " * " + right + ")"
            elif opcode == "div":
                if left == "0":
                    return 0
                if right == "1":
                    return left
                return "(" + left + " // " + right + ")"
            elif opcode == "mod":
                return "(" + left + " % " + right + ")"
            elif opcode == "eql":
                if right == "0":
                    if m := re.match(r"\((\w*|\(.*\)) == (\w*|\(.*\))\)", left):
                        return "(" + m.group(1) + " != " + m.group(2) + ")"
                    return "(not " + left + ")"
                if left == "0":
                    if m := re.match(r"\((\w*|\(.*\)) == (\w*|\(.*\))\)", right):
                        return "(" + m.group(1) + " != " + m.group(2) + ")"
                    return "(not " + right + ")"
                return "(" + left + " == " + right + ")"
            else:
                raise ValueError
    return var


# solve each code block for z and compile the resulting expression
blockf = [compile(solve(block, 'z'), "<string>", "eval") for block in DATA]

cache = set()
cache_hit = cache.__contains__
cache_add = cache.add


def DFS(z: int, n: int):
    # we are done if we have one input for every block
    if n == N:
        if z == 0:
            return 0
        return

    # check for cache hits
    key = z * N + n  # (z, n)
    if cache_hit(key):
        return
    cache_add(key)

    # test all possible inputs for the n-the block
    f = blockf[n]
    for inp in INPUT_RANGE:
        result = DFS(eval(f, {}, {"z": z, "inp": inp}), n + 1)
        if result is not None:  # we found a solution and are done
            return result + inp * 10 ** (N - 1 - n)


# Part One

INPUT_RANGE = (9, 8, 7, 6, 5, 4, 3, 2, 1)
cache.clear()
print("Part One", DFS(0, 0))

# Part Two

INPUT_RANGE = (1, 2, 3, 4, 5, 6, 7, 8, 9)
cache.clear()
print("Part Two", DFS(0, 0))
