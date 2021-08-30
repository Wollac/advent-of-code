"""
--- Day 23: Category Six ---
https://adventofcode.com/2019/day/23
"""
import aocd

from .intcode import IntComputer

PROGRAM = [int(n) for n in aocd.data.split(",")]


def part_a():
    comps = [IntComputer(PROGRAM, (index,)) for index in range(50)]

    while True:
        for comp in comps:
            try:
                comp.run(IntComputer.op_output)
            except IndexError:
                comp.input.append(-1)  # no packet in the queue

            if len(comp.output) >= 3:
                dest, *pkt = (comp.output.popleft() for _ in range(3))
                if dest == 255:
                    return pkt[1]
                else:
                    comps[dest].input.extend(pkt)


print("Part One:", part_a())


def empty(queue):
    return not queue or queue[0] == -1


def part_b():
    nat, last_nat = None, None
    comps = [IntComputer(PROGRAM, (index,)) for index in range(50)]

    while True:
        for index, comp in enumerate(comps):
            try:
                comp.run(IntComputer.op_output)
            except IndexError:
                # if the network is idle use the NAT
                if nat and index == 0 and all(empty(c.input) and not c.output for c in comps):
                    comp.input.extend(nat)
                    if last_nat and last_nat[1] == nat[1]:
                        return nat[1]
                    last_nat = nat
                else:
                    comp.input.append(-1)  # no packet in the queue

            if len(comp.output) >= 3:
                dest, *pkt = (comp.output.popleft() for _ in range(3))
                if dest == 255:
                    nat = pkt
                else:
                    comps[dest].input.extend(pkt)


print("Part Two:", part_b())
