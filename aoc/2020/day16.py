"""
--- Day 16: Ticket Translation ---
https://adventofcode.com/2020/day/16
"""
import re
from math import prod

import aocd

fields_raw, my_ticket_raw, nearby_tickets_raw = aocd.data.split("\n\n")

fields = {name: [(int(l1), int(u1)), (int(l2), int(u2))] for name, l1, u1, l2, u2 in
          re.findall(r"([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)", fields_raw)}
_, my_ticket = my_ticket_raw.splitlines()
my_ticket = [int(n) for n in my_ticket.split(",")]
_, *nearby_tickets = nearby_tickets_raw.splitlines()
nearby_tickets = [[int(x) for x in line.split(",")] for line in nearby_tickets]


# Part One

def valid(v, ranges):
    return any(x <= v <= y for x, y in ranges)


def hasvalid(v):
    return any(valid(v, ranges) for ranges in fields.values())


sol1 = sum(v for ticket in nearby_tickets for v in ticket if not hasvalid(v))
print("Part One: The ticket scanning error rate is", sol1)

# Part Two

valid_tickets = list(filter(lambda t: all(hasvalid(v) for v in t), nearby_tickets))

# compute the set of possible field names for each field index
field_options = [{name for name, ranges in fields.items() if all(valid(ticket[i], ranges) for ticket in valid_tickets)}
                 for i, _ in enumerate(fields)
                 ]

# solve greedily, this seems to be sufficient for the provided input where no backtracking is needed
known = {}
while len(known) < len(fields):
    for i, options in enumerate(field_options):
        unknowns = options.difference(known.keys())
        if len(unknowns) == 1:
            known[unknowns.pop()] = i
            break

sol2 = prod(my_ticket[i] for name, i in known.items() if name.startswith("departure"))
print("Part Two: The product of the 'departure*' fields is", sol2)
