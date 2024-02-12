DIR = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}


def get_neighbors(cur):
    return [tuple(map(lambda i, j: i + j, cur, dir)) for dir in DIR.values()]


if __name__ == '__main__':
    f = open("input.txt", "r")

    instructions = [line.split(" ") for line in f.read().splitlines()]
    minX, maxX, minY, maxY = 0, 0, 0, 0
    cur = (0, 0)
    for instruction in instructions:
        cur = tuple(map(lambda i, j: i + j *
                    int(instruction[1]), cur, DIR[instruction[0]]))
        print(cur)
        if cur[0] < minX:
            minX = cur[0]
        if cur[1] < minY:
            minY = cur[1]
        if cur[0] > maxX:
            maxX = cur[0]
        if cur[1] > maxY:
            maxY = cur[1]
    print(minX, maxX, minY, maxY)
    grid = [["." for _ in range(maxX - minX + 1)]
            for _ in range(maxY - minY + 1)]

    print(cur)
    cur = (-minX, -minY)
    for instruction in instructions:
        for _ in range(int(instruction[1])):
            cur = tuple(map(lambda i, j: i + j, cur, DIR[instruction[0]]))
            grid[cur[1]][cur[0]] = "#"
    print(*("".join(line) for line in grid), sep="\n")
    cur = tuple(map(lambda i, j: i + j, cur, (1, 1)))
    to_visit = [cur]
    while len(to_visit) > 0:
        _cur = to_visit.pop()
        grid[_cur[1]][_cur[0]] = "#"
        for neighbor in get_neighbors(_cur):
            if grid[neighbor[1]][neighbor[0]] == ".":
                to_visit.append(neighbor)
    print(*("".join(line) for line in grid), sep="\n")
    print(sum(line.count("#") for line in grid))
