"""
--- Day 13: Care Package ---
https://adventofcode.com/2019/day/13
"""
import aocd
import numpy as np

from .intcode import IntComputer

program = [int(n) for n in aocd.data.split(",")]

output = np.array(IntComputer(program).run()).reshape((-1, 3))  # each single output consists of tuples of 3 values
print("Part One:", np.count_nonzero(output[:, -1] == 2))

# start the actual game
game = IntComputer([2] + program[1:])
paddle = (0, 0)  # set to an arbitrary position
score = 0
while True:
    try:
        # fetch one output tuple at a time
        x, y, tile_id = (game.run(until=IntComputer.op_output).popleft() for _ in range(3))
    except IntComputer.Halt:
        break
    if x == -1 and y == 0:  # update score
        score = tile_id
    elif tile_id == 3:  # paddle
        paddle = (x, y)
    elif tile_id == 4:  # ball
        ball = (x, y)
        game.input.append(np.sign(ball[0] - paddle[0]))  # move the paddle in the direction of the ball

print("Part Two:", score)
