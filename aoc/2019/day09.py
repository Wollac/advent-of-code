"""
--- Day 9: Sensor Boost ---
https://adventofcode.com/2019/day/9
"""
import aocd

from .intcode import IntComputer

program = [int(n) for n in aocd.data.split(",")]

print("Part One:", IntComputer(program, [1]).run().popleft())
print("Part Two:", IntComputer(program, [2]).run().popleft())
