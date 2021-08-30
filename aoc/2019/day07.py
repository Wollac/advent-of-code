"""
--- Day 7: Amplification Circuit ---
https://adventofcode.com/2019/day/7
"""
from collections import deque
from functools import reduce
from itertools import permutations

import aocd

program = [int(n) for n in aocd.data.split(",")]


class IntComputer:
    class Halt(Exception):
        pass

    def __init__(self, mem, inputs=()):
        self.pc = 0
        self.mem = mem.copy()
        self.input = deque(inputs)
        self.output = deque()
        self.__last_op = None
        self.ops = {
            1: self.op_add,
            2: self.op_mul,
            3: self.op_input,
            4: self.op_output,
            5: self.op_jump_true,
            6: self.op_jump_false,
            7: self.op_lt,
            8: self.op_eq,
            99: self.op_halt,
        }

    def op_add(self, x, y, z):
        self.mem[z] = self.mem[x] + self.mem[y]

    def op_mul(self, x, y, z):
        self.mem[z] = self.mem[x] * self.mem[y]

    def op_input(self, x):
        self.mem[x] = self.input.popleft()

    def op_output(self, x):
        self.output.append(self.mem[x])

    def op_jump_true(self, x, y):
        if self.mem[x]:
            self.pc = self.mem[y]

    def op_jump_false(self, x, y):
        if not self.mem[x]:
            self.pc = self.mem[y]

    def op_lt(self, x, y, z):
        self.mem[z] = int(self.mem[x] < self.mem[y])

    def op_eq(self, x, y, z):
        self.mem[z] = int(self.mem[x] == self.mem[y])

    def op_halt(self):
        raise IntComputer.Halt

    def step(self):
        opcode = self.mem[self.pc]
        self.pc += 1
        op = self.ops[opcode % 100]
        nargs = op.__code__.co_argcount - 1
        modes = str(opcode // 100).zfill(nargs)[::-1]
        args = []
        for i in range(nargs):
            if modes[i] == '0':
                args.append(self.mem[self.pc])
            elif modes[i] == '1':
                args.append(self.pc)
            else:
                raise Exception(f"invalid  mode '{modes[i]}'")
            self.pc += 1
        self.__last_op = op
        op(*args)

    def run(self, until=op_halt):
        while True:
            try:
                self.step()
            except IntComputer.Halt:
                if until is not IntComputer.op_halt:
                    raise IntComputer.Halt
            if self.__last_op.__func__ is until:
                return self.output


def amplifier(x, setting):
    return IntComputer(program, inputs=[setting, x]).run().popleft()


print("Part One:", max(reduce(amplifier, settings, 0) for settings in permutations(range(0, 5))))


def thruster(x, settings):
    amps = [IntComputer(program, inputs=[setting]) for setting in settings]
    # link the output of each amplifier to the input of its successor
    for amp1, amp2 in zip(amps, amps[1:] + amps[:1]):
        amp1.output = amp2.input

    amps[0].input.append(x)
    while True:
        for amp in amps:
            try:
                amp.run(until=IntComputer.op_output)
            except IntComputer.Halt:
                # run until the last amplifier has halted
                if amp == amps[-1]:
                    return amp.output.popleft()


print("Part Two:", max(thruster(0, settings) for settings in permutations(range(5, 10))))
