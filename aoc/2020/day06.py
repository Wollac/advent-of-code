"""
--- Day 6: Custom Customs ---
https://adventofcode.com/2020/day/6
"""
import aocd

DATA = [[{answer for answer in person} for person in group.splitlines()] for group in aocd.data.split("\n\n")]

sum1, sum2 = 0, 0
for group in DATA:
    answered = set().union(*group)
    sum1 += len(answered)
    sum2 += len(answered.intersection(*group))

print("Part One: The sum of all the questions answered by each group is %d" % sum1)
print("Part Two: The sum of all the questions answered by every person in each group is %d" % sum2)
