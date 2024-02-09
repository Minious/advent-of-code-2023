import re

f = open("input.txt", "r")

s = 0

gears = {}

lines = list(f)
for j, line_nl in enumerate(lines):
    line = line_nl[:-1]
    for i, c in enumerate(line):
        if c.isdigit() and (i == 0 or not line[i-1].isdigit()):
            number = re.search("[0-9]+", line[i:]).group()
            for y in range(j-1, j+2):
                for x in range(i-1, i+len(number)+1):
                    if x >= 0 and y >= 0 and x < len(line) and y < len(lines):
                        el = lines[y][x]
                        if el == "*":
                            if (y, x) not in gears:
                                gears[(y, x)] = []
                            gears[(y, x)] += [int(number)]
for numbers in gears.values():
    if len(numbers) == 2:
        s += numbers[0] * numbers[1]
print(s)
