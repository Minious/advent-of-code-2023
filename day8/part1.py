import re

f = open("input.txt", "r")

lines = f.read().splitlines()

instructions = lines[0]
nodes = {t[0]: (t[1], t[2]) for t in (re.search(
    "([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line).groups() for line in lines[2:])}
cur_node = "AAA"
count = 0
while cur_node != "ZZZ":
    instruction = instructions[count % len(instructions)]
    if instruction == "L":
        cur_node = nodes[cur_node][0]
    elif instruction == "R":
        cur_node = nodes[cur_node][1]
    count += 1

print(count)
