"""
--- Day 19: Monster Messages ---
https://adventofcode.com/2020/day/19
"""
import re

import aocd

rule_pattern = re.compile(r"(\d+): (.+)")
base_pattern = re.compile(r"\"([a-z])\"")

rules_raw, messages_raw = aocd.data.split("\n\n")

rules = {}
for rule_number, rule_raw in rule_pattern.findall(rules_raw):
    if m := base_pattern.match(rule_raw):
        rules[int(rule_number)] = m[1]
    else:
        rules[int(rule_number)] = [tuple(int(n) for n in sub.strip().split(" ")) for sub in rule_raw.split("|")]
messages = [m for m in messages_raw.splitlines()]


# Part One

def matchsucc(rule_numbers, string):
    # matches string successively against all the rules with the given numbers
    parts = {""}
    for n in rule_numbers:
        parts = {p + m for p in parts for m in match(n, string[len(p):])}
    return parts


def match(n, string):
    rule = rules[n]
    if type(rule) == str:
        return {rule} if string.startswith(rule) else set()
    # match against any of the sub-rules
    return set.union(*(matchsucc(sub, string) for sub in rule))


rule = 0
sol1 = sum(m in match(rule, m) for m in messages)
print(f"Part One: The number of messages that completely match rule '{rule}' is", sol1)

# Part Two

rules[8] = [(42,), (42, 8)]
rules[11] = [(42, 31), (42, 11, 31)]

sol2 = sum(m in match(rule, m) for m in messages)
print(f"Part Two: The number of messages that completely match rule '{rule}' is", sol2)
