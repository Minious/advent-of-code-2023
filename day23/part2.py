import math

dirs = [
    (0, 1), (0, -1), (-1, 0), (1, 0)
]


def is_valid_position(position, grid):
    if position[0] < 0 or position[1] < 0 or position[0] >= len(grid[0]) or position[1] >= len(grid):
        return False
    return grid[position[1]][position[0]] in [".", ">", "<", "^", "v"]


_best_length = 0


def is_intersection(grid, position):
    if position == (1, 0) or position == (len(grid[0]) - 2, len(grid) - 1):
        return True
    if not is_valid_position(position, grid):
        return False
    neighbors = [tuple(map(lambda x, y: x + y, position, dir))
                 for dir in dirs]
    valid_neighbors = [
        neighbor for neighbor in neighbors if is_valid_position(neighbor, grid)]
    return len(valid_neighbors) >= 3


def get_paths_until_intersection(origin, grid):
    paths = {}
    for starting_dir in dirs:
        current = tuple(map(lambda x, y: x + y, origin, starting_dir))
        if not is_valid_position(current, grid):
            continue
        path = [origin, current]
        while not is_intersection(grid, current):
            for dir in dirs:
                next_pos = tuple(map(lambda x, y: x + y, current, dir))
                if next_pos not in path and is_valid_position(next_pos, grid):
                    current = next_pos
                    path += [current]
                    break
        paths[current] = path
    return paths


def build_graph(grid):
    graph = {}
    intersections = [(1, 0)]
    idx = 0
    while len(intersections) > idx:
        intersection = intersections[idx]
        paths = get_paths_until_intersection(intersection, grid)
        for path in paths:
            if intersection not in graph:
                graph[intersection] = {}
            graph[intersection][path] = len(paths[path]) - 1
            if path not in intersections:
                intersections.append(path)
        idx += 1
    return graph


def get_path(graph, position, previous_path=[]):
    global _best_length
    if position == (len(grid[0]) - 2, len(grid) - 1):
        return 0, []
    best_length = - math.inf
    best_path = []
    for next_pos in graph[position]:
        if next_pos in previous_path:
            continue
        length, path = get_path(graph, next_pos, previous_path + [next_pos])
        if length + graph[position][next_pos] > best_length:
            best_length = length + graph[position][next_pos]
            best_path = path + [next_pos]
    if best_length > _best_length:
        _best_length = best_length
        print(_best_length, best_path)
    return best_length, best_path


if __name__ == '__main__':
    f = open("input.txt", "r")

    grid = [[c for c in line] for line in f.read().splitlines()]
    graph = build_graph(grid)
    # print(*graph.items(), sep="\n")
    best_length, best_path = get_path(graph, (1, 0), previous_path=[])
    print(best_length)
