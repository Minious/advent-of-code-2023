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
    # print(*["".join(line) for line in _map], sep="\n")
    cur_pos, prev_pos = get_next_pos(
        cur_pos, prev_pos, lines[cur_pos[1]][cur_pos[0]]), cur_pos
    step += 1
print(*["".join(line) for line in _map], sep="\n")
print(path)
print(int(step / 2))
