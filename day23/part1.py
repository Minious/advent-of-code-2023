import math
import time
import copy

dirs = [
    (0, 1), (0, -1), (-1, 0), (1, 0)
]


def is_neighbor_valid(current, neighbor, grid):
    if neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] >= len(grid[0]) or neighbor[1] >= len(grid):
        return False
    if grid[neighbor[1]][neighbor[0]] == "#":
        return False
    if grid[neighbor[1]][neighbor[0]] == ">" and current[0] == neighbor[0] + 1:
        return False
    if grid[neighbor[1]][neighbor[0]] == "<" and current[0] == neighbor[0] - 1:
        return False
    if grid[neighbor[1]][neighbor[0]] == "v" and current[1] == neighbor[1] + 1:
        return False
    if grid[neighbor[1]][neighbor[0]] == "^" and current[1] == neighbor[1] - 1:
        return False
    return True


def get_neighbors(current, grid):
    return [neighbor for neighbor in [tuple(map(lambda i, j: i + j, current, dir))
                                      for dir in dirs] if is_neighbor_valid(current, neighbor, grid)]


def build_graph(grid, start):
    graph = {}
    reversed_graph = {}
    queue = [start]
    while len(queue) > 0:
        current = queue.pop(0)
        neighbors = get_neighbors(current, grid)
        if current not in graph:
            graph[current] = {}
        for neighbor in neighbors:
            if current not in reversed_graph or neighbor not in reversed_graph[current]:
                queue.append(neighbor)
                graph[current][neighbor] = -1
                if neighbor not in reversed_graph:
                    reversed_graph[neighbor] = {}
                reversed_graph[neighbor][current] = -1
    return graph


def reverse_graph(graph):
    r = {}
    for n in graph:
        for m in graph[n]:
            if m not in r:
                r[m] = {}
            r[m][n] = graph[n][m]
    return r


def topological_sort(graph, start):
    _graph = copy.deepcopy(graph)
    reversed_graph = reverse_graph(_graph)
    l = []
    s = [start]
    while len(s) > 0:
        n = s.pop()
        l.append(n)
        for m in _graph[n]:
            del reversed_graph[m][n]
            if len(reversed_graph[m]) == 0:
                s.append(m)
    return l


def longest_path(topo, graph, source):
    dist = {v: math.inf for v in topo}
    prev = {v: None for v in topo}

    dist[source] = 0

    for current in topo:
        for neighbor in graph[current]:
            w = graph[current][neighbor]
            if dist[neighbor] > dist[current] + w:
                dist[neighbor] = dist[current] + w
                prev[neighbor] = current
    return dist, prev


def get_path(prev, dest):
    path = []
    cur = dest
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))


if __name__ == '__main__':
    f = open("input.txt", "r")

    grid = [[c for c in line] for line in f.read().splitlines()]
    graph = build_graph(grid, (1, 0))
    topo = topological_sort(graph, (1, 0))
    dist, prev = longest_path(topo, graph, (1, 0))
    path = get_path(prev, (len(grid[0]) - 2, len(grid) - 1))
    print(len(path) - 1)
