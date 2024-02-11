def move_up(grid):
    for i, line in enumerate(grid[:-1]):
        for j, c in enumerate(line):
            if grid[i][j] == "." and grid[i + 1][j] == "O":
                grid[i][j], grid[i + 1][j] = "O", "."


def rotate_grid(grid):
    return list(list(l) for l in zip(*grid[::-1]))


f = open("input.txt", "r")

grid = [[c for c in line] for line in f.read().splitlines()]
memo = {}
steps = 1000000000
for i in range(steps):
    print(i, sum((i + 1) * line.count("O")
          for i, line in enumerate(grid[::-1])))
    key = tuple(tuple(l[:]) for l in grid)
    if key in memo:
        # grid = [l[:] for l in memo[key][1]]
        break
    else:
        for _ in range(4):
            for _ in range(len(grid)):
                move_up(grid)
            grid = rotate_grid(grid)
        copy = [l[:] for l in grid]
        memo[key] = (i, copy)
cycle = i - memo[key][0]
print("CYCLE =", cycle)
rem_steps = steps - i
print("REM STEPS =", rem_steps)
steps_to_go = rem_steps % cycle
print("STEPS TO GO =", steps_to_go)
for i in range(steps_to_go):
    for _ in range(4):
        for _ in range(len(grid)):
            move_up(grid)
        grid = rotate_grid(grid)

print(*("".join(line) for line in grid), sep="\n")

s = sum((i + 1) * line.count("O") for i, line in enumerate(grid[::-1]))
print(s)
