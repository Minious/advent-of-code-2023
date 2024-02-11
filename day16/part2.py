def get_dirs(dir, el):
    match el:
        case ".":
            return [dir]
        case "/":
            return [(-dir[1], -dir[0])]
        case "\\":
            return [(dir[1], dir[0])]
        case "|":
            if dir[0] == 0:
                return [dir]
            else:
                return [(0, 1), (0, -1)]
        case "-":
            if dir[1] == 0:
                return [dir]
            else:
                return [(-1, 0), (1, 0)]


def display_grid(_grid, beams):
    grid = [l[:] for l in _grid]
    for beam in beams:
        if grid[beam[1]][beam[0]] == ".":
            dirs = beams[beam]
            if len(dirs) > 1:
                grid[beam[1]][beam[0]] = str(len(dirs))
            else:
                dir = dirs[0]
                dir_char = {
                    (-1, 0): "<",
                    (1, 0): ">",
                    (0, -1): "^",
                    (0, 1): "v",
                }[dir]
                grid[beam[1]][beam[0]] = dir_char
    print(*("".join(l) for l in grid), sep="\n")


def display_energy(_grid, beams):
    grid = [["." for _ in range(len(_grid[0]))] for _ in range(len(_grid))]
    for beam in beams:
        grid[beam[1]][beam[0]] = "#"
    print(*("".join(l) for l in grid), sep="\n")


def get_beams(initial_beam, grid):
    beams = {}
    current_beams = [initial_beam]

    while len(current_beams) > 0:
        current_beam = current_beams.pop()
        if current_beam["pos"] not in beams:
            beams[current_beam["pos"]] = []
        if current_beam["dir"] not in beams[current_beam["pos"]]:
            beams[current_beam["pos"]].append(current_beam["dir"])
            new_pos = tuple(
                map(lambda i, j: i + j, current_beam["pos"], current_beam["dir"]))
            if new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < len(grid[0]) and new_pos[1] < len(grid):
                new_dirs = get_dirs(
                    current_beam["dir"], grid[new_pos[1]][new_pos[0]])
                for new_dir in new_dirs:
                    new_beam = {"pos": new_pos, "dir": new_dir}
                    current_beams.append(new_beam)
    return beams


f = open("input.txt", "r")

grid = [[c for c in line] for line in f.read().splitlines()]

best = None
best_beams = None
best_starting_beam = None

for i in range(len(grid)):
    initial_beam = {"pos": (-1, i), "dir": (1, 0)}
    beams = get_beams(initial_beam, grid)
    energy = len(beams) - 1
    if best == None or best < energy:
        best = energy
        best_beams = beams
        best_starting_beam = initial_beam
    initial_beam = {"pos": (len(grid), i), "dir": (-1, 0)}
    beams = get_beams(initial_beam, grid)
    energy = len(beams) - 1
    if best == None or best < energy:
        best = energy
        best_beams = beams
        best_starting_beam = initial_beam
for i in range(len(grid[0])):
    initial_beam = {"pos": (i, -1), "dir": (0, 1)}
    beams = get_beams(initial_beam, grid)
    energy = len(beams) - 1
    if best == None or best < energy:
        best = energy
        best_beams = beams
        best_starting_beam = initial_beam
    initial_beam = {"pos": (i, len(grid[0])), "dir": (0, -1)}
    beams = get_beams(initial_beam, grid)
    energy = len(beams) - 1
    if best == None or best < energy:
        best = energy
        best_beams = beams
        best_starting_beam = initial_beam

display_grid(grid, best_beams)
print()
display_energy(grid, best_beams)
print()
print(best)
print(best_starting_beam)
