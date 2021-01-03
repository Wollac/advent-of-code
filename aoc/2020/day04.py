"""
--- Day 4: Passport Processing ---
https://adventofcode.com/2020/day/4
"""
import re

import aocd

passports = []
passport = {}
for line in aocd.data.splitlines():
    if not line.strip():
        if passport:
            passports.append(passport)
            passport = {}
        continue

    for e in line.split():
        key, value = e.split(":")
        passport[key] = value

if passport:
    passports.append(passport)

required = {
    "byr": r"(\d{4})$",
    "iyr": r"(\d{4})$",
    "eyr": r"(\d{4})$",
    "hgt": r"([1-9]\d{1,2})(cm|in)$",
    "hcl": r"#([0-9a-f]{6})$",
    "ecl": r"(amb|blu|brn|gry|grn|hzl|oth)$",
    "pid": r"(\d{9})$",
}


# Part One

def valid1(passport):
    for key in required:
        if key not in passport:
            return False
    return True


count1 = sum(valid1(passport) for passport in passports)
print("Part One: The number of valid passports is %d" % count1)


# Part Two

def validkey(key, value):
    m = re.match(required[key], value)
    if m is None:
        return False
    if key == "byr":
        v = int(m.group(1))
        if v < 1920 or v > 2002:
            return False
    elif key == "iyr":
        v = int(m.group(1))
        if v < 2010 or v > 2020:
            return False
    elif key == "eyr":
        v = int(m.group(1))
        if v < 2020 or v > 2030:
            return False
    elif key == "hgt":
        v, d = int(m.group(1)), m.group(2)
        if d == "cm":
            return 150 <= v <= 193
        elif d == "in":
            return 59 <= v <= 76
        else:
            return False
    return True


def valid2(passport):
    for key in required:
        if key not in passport:
            return False
        if not validkey(key, passport[key]):
            return False
    return True


count2 = sum(valid2(passport) for passport in passports)
print("Part Two: The number of valid passports is %d" % count2)
