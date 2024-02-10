import re


def get_next_pos(cur_pos, prev_pos, pipe):
    match(pipe):
        case "|":
            return (cur_pos[0], cur_pos[1] + cur_pos[1] - prev_pos[1])
        case "-":
            return (cur_pos[0] + cur_pos[0] - prev_pos[0], cur_pos[1])
        case "L":
            if cur_pos[0] == prev_pos[0]:
                return (cur_pos[0] + 1, cur_pos[1])
            elif cur_pos[1] == prev_pos[1]:
                return (cur_pos[0], cur_pos[1] - 1)
        case "J":
            if cur_pos[0] == prev_pos[0]:
                return (cur_pos[0] - 1, cur_pos[1])
            elif cur_pos[1] == prev_pos[1]:
                return (cur_pos[0], cur_pos[1] - 1)
        case "7":
            if cur_pos[0] == prev_pos[0]:
                return (cur_pos[0] - 1, cur_pos[1])
            elif cur_pos[1] == prev_pos[1]:
                return (cur_pos[0], cur_pos[1] + 1)
        case "F":
            if cur_pos[0] == prev_pos[0]:
                return (cur_pos[0] + 1, cur_pos[1])
            elif cur_pos[1] == prev_pos[1]:
                return (cur_pos[0], cur_pos[1] + 1)


def is_inside_loop(loop, point):
    counter = 0

    p1 = loop[0]
    for i in range(1, len(loop) + 1):
        p2 = loop[i % len(loop)]
        if point[1] > min(p1[1], p2[1]) and point[1] <= max(p1[1], p2[1]) and point[0] <= max(p1[0], p2[0]) and p1[1] != p2[1]:
            xinters = (point[1] - p1[1]) * \
                (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
            if p1[0] == p2[0] or point[0] <= xinters:
                counter += 1
        p1 = p2
    return counter % 2 == 1


f = open("input.txt", "r")

lines = f.read().splitlines()
_map = [["." for _ in range(len(lines[0]))] for _ in range(len(lines))]
path = []

cur_pos = next((line.index("S"), i)
               for i, line in enumerate(lines) if "S" in line)
_map[cur_pos[1]][cur_pos[0]] = lines[cur_pos[1]][cur_pos[0]]
path += [cur_pos]

cur_pos, prev_pos = (cur_pos[0] + 1, cur_pos[1]), cur_pos
step = 1
while lines[cur_pos[1]][cur_pos[0]] != "S":
    _map[cur_pos[1]][cur_pos[0]] = lines[cur_pos[1]][cur_pos[0]]
    path += [cur_pos]
    cur_pos, prev_pos = get_next_pos(
        cur_pos, prev_pos, lines[cur_pos[1]][cur_pos[0]]), cur_pos
    step += 1
print(path)
print(int(step / 2))

c = 0
for j in range(len(lines)):
    for i in range(len(lines[j])):
        el = lines[j][i]
        if (i, j) not in path:
            if is_inside_loop(path, (i+.25, j+.25)):
                c += 1
                _map[j][i] = "I"
            else:
                _map[j][i] = "O"
print(*["".join(line) for line in _map], sep="\n")
print(c)
