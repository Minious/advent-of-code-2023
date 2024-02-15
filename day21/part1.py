dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

if __name__ == '__main__':
    f = open("input.txt", "r")

    grid = [[c for c in line] for line in f.read().splitlines()]

    start = [(line.index("S"), i)
             for i, line in enumerate(grid)
             if "S" in line][0]
    positions = [start]
    print(start)
    steps = 64
    for _ in range(steps):
        new_positions = []
        for position in positions:
            for dir in dirs:
                new_position = tuple(map(lambda i, j: i + j, position, dir))
                if grid[new_position[1]][new_position[0]] != "#" and new_position not in new_positions:
                    new_positions.append(new_position)
        positions = new_positions
    print(len(positions))
