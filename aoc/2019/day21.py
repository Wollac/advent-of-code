"""
--- Day 21: Springdroid Adventure ---
https://adventofcode.com/2019/day/21
"""
import aocd

from .intcode import IntComputer

PROGRAM = [int(n) for n in aocd.data.split(",")]


def run(code):
    comp = IntComputer(PROGRAM, (ord(c) for c in code))
    output = comp.run()
    return output.pop(), "".join(chr(c) for c in output)


def jump1(sensor):
    # there are holes in between and we can safely land
    if (not sensor[1] or not sensor[2] or not sensor[3]) and sensor[4]:
        return True
    return False


code = """\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

val, message = run(code)
print(message)
print("Part One:", val)


def jump2(sensor):
    # there are holes in between and (we can walk one step after the jump or jump directly again) and we can safely land
    if (not sensor[1] or not sensor[2] or not sensor[3]) and (sensor[5] or sensor[8]) and sensor[4]:
        return True
    return False


code = """\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
NOT E T
NOT T T
OR H T
AND T J
AND D J
RUN
"""

val, message = run(code)
print(message)
print("Part Two:", val)
