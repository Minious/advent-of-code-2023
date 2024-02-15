import math

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

if __name__ == '__main__':
    f = open("input_simple2.txt", "r")

    grid = [[c for c in line] for line in f.read().splitlines()]

    steps = 39
    x = 1 + math.ceil((steps - (len(grid) - 1) / 2) / len(grid)) * 2
    print("x", x)
    grid = [[grid[j % len(grid)][i % len(grid)] for i in range(len(grid) * x)]
            for j in range(len(grid) * x)]

    start = (int((len(grid) - 1)/2), int((len(grid) - 1)/2))
    positions = [start]
    print(start)
    for _ in range(steps):
        new_positions = []
        for position in positions:
            for dir in dirs:
                new_position = tuple(map(lambda i, j: i + j, position, dir))
                if grid[new_position[1]][new_position[0]] != "#" and new_position not in new_positions:
                    new_positions.append(new_position)
        positions = new_positions
    for pos in positions:
        grid[pos[1]][pos[0]] = "O"
    print(*(" ".join(l) for l in grid), sep="\n")
    print(len(positions))
