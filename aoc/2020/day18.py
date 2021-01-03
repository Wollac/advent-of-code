"""
--- Day 18: Operation Order ---
https://adventofcode.com/2020/day/18
"""
import re
from collections import deque

import aocd

DATA = aocd.data.splitlines()

token_pattern = re.compile(r"(\d+|[\(\)\+\*])")


def rpn(expr: str, prec: dict):
    """
    Shunting-yard algorithm parses the expression and returns the operations in reverse Polish notation.
    https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    """
    output = deque()
    stack = deque()
    for token in token_pattern.findall(expr):
        if token == "+" or token == "*":
            while stack and stack[-1] != "(" and prec[stack[-1]] >= prec[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
        else:
            output.append(int(token))
    while stack:
        output.append(stack.pop())
    return output


def eval_rpn(stack):
    t = stack.pop()
    if t == "+":
        return eval_rpn(stack) + eval_rpn(stack)
    if t == "*":
        return eval_rpn(stack) * eval_rpn(stack)
    return t


# Part One

# addition and multiplication have equal precedence
precedence = {"+": 1, "*": 1}

sol1 = sum([eval_rpn(rpn(expr, precedence)) for expr in DATA])
print(f"Part One: The sum of all the results with precedence {precedence} is", sol1)

# Part Two

# addition has greater precedence than multiplication
precedence = {"+": 2, "*": 1}

sol2 = sum([eval_rpn(rpn(expr, precedence)) for expr in DATA])
print(f"Part Two: The sum of all the results with precedence {precedence} is", sol2)
