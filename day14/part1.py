def move_up(grid):
    for i, line in enumerate(grid[:-1]):
        for j, c in enumerate(line):
            if grid[i][j] == "." and grid[i + 1][j] == "O":
                grid[i][j], grid[i + 1][j] = "O", "."


f = open("input.txt", "r")

grid = [[c for c in line] for line in f.read().splitlines()]
for _ in range(len(grid)):
    move_up(grid)
print(*("".join(line) for line in grid), sep="\n")

s = sum((i + 1) * line.count("O") for i, line in enumerate(grid[::-1]))
print(s)
