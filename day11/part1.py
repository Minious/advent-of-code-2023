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


universe = [[c for c in line] for line in f.read().splitlines()]

expand_universe(universe)
print("UNIVERSE")
print(*("".join(line) for line in universe), sep="\n")

stars = [(i, j) for j in range(len(universe))
         for i in range(len(universe[j])) if universe[j][i] == "#"]
print("STARS")
print(stars)

total = 0
for star1_idx in range(len(stars)):
    for star2_idx in range(star1_idx + 1, len(stars)):
        star1 = stars[star1_idx]
        star2 = stars[star2_idx]
        distance = abs(star2[1] - star1[1]) + abs(star2[0] - star1[0])
        total += distance
print(total)
