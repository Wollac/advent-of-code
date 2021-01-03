"""
--- Day 11: Seating System ---
https://adventofcode.com/2020/day/11
"""
import aocd

seats = [[c == 'L' for c in line] for line in aocd.data.splitlines()]
max_rows = len(seats)
max_columns = len(seats[0])

dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (1, -1), (0, -1)]


def neighbors(occupied, x, y, level):
    c = 0
    for dx, dy in dirs:
        for s in range(1, level + 1):
            nx, ny = x + s * dx, y + s * dy
            if nx < 0 or nx >= max_columns or ny < 0 or ny >= max_rows:
                break
            if not seats[ny][nx]:
                continue
            if occupied[ny][nx]:
                c += 1
            break
    return c


def run(empty_threshold, level=1):
    occupied = [[False] * max_columns for _ in range(max_rows)]
    while True:
        tmp = [[False] * max_columns for _ in range(max_rows)]
        for y in range(max_rows):
            for x in range(max_columns):
                if not seats[y][x]:
                    continue
                if occupied[y][x]:
                    tmp[y][x] = neighbors(occupied, x, y, level) < empty_threshold
                else:
                    tmp[y][x] = neighbors(occupied, x, y, level) < 1
        if tmp == occupied:
            break
        occupied = tmp
    return occupied


# Part One

count1 = sum([row.count(True) for row in run(4)])
print("Part One: The number of occupied seats is %d" % count1)

# Part Two

count2 = sum([row.count(True) for row in run(5, len(seats))])
print("Part Two: The number of occupied seats is %d" % count2)
