f = open("input.txt", "r")


def expand_universe(universe):
    for line_idx in range(len(universe) - 1, -1, -1):
        line = universe[line_idx]
        if all(c == "." for c in line):
            universe.insert(line_idx, line[:])
    for column_idx in range(len(universe[0]) - 1, -1, -1):
        column = [line[column_idx] for line in universe]
        # print(column)
        if all(c == "." for c in column):
            for line in universe:
                line.insert(column_idx, ".")


def get_empty_lines_between(y1, y2, empty_lines_idx):
    c = 0
    for line_idx in range(y1 + 1, y2):
        if line_idx in empty_lines_idx:
            c += 1
    return c


def get_empty_columns_between(x1, x2, empty_columns_idx):
    c = 0
    for column_idx in range(x1 + 1, x2):
        if column_idx in empty_columns_idx:
            c += 1
    return c


def get_empty_lines_idx(universe):
    idx = []
    for line_idx in range(len(universe)):
        line = universe[line_idx]
        if all(c == "." for c in line):
            idx.append(line_idx)
    return idx


def get_empty_columns_idx(universe):
    idx = []
    for column_idx in range(len(universe[0])):
        column = [line[column_idx] for line in universe]
        if all(c == "." for c in column):
            idx.append(column_idx)
    return idx


universe = [[c for c in line] for line in f.read().splitlines()]

# expand_universe(universe)
print("UNIVERSE")
print(*("".join(line) for line in universe), sep="\n")

stars = [(i, j) for j in range(len(universe))
         for i in range(len(universe[j])) if universe[j][i] == "#"]
print("STARS")
print(stars)

empty_lines_idx = get_empty_lines_idx(universe)
empty_columns_idx = get_empty_columns_idx(universe)

total = 0
expansion = 1000000
for star1_idx in range(len(stars)):
    for star2_idx in range(star1_idx + 1, len(stars)):
        star1 = stars[star1_idx]
        star2 = stars[star2_idx]
        distX = abs(star2[0] - star1[0])
        distY = abs(star2[1] - star1[1])
        empty_lines = get_empty_lines_between(
            min(star2[1], star1[1]), max(star2[1], star1[1]), empty_lines_idx)
        empty_columns = get_empty_columns_between(
            min(star2[0], star1[0]), max(star2[0], star1[0]), empty_columns_idx)
        distance = (distX - empty_columns) + empty_columns * \
            expansion + (distY - empty_lines) + empty_lines * expansion
        total += distance
print(total)
