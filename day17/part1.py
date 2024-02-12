import math
from itertools import groupby
import time
from my_queue import MinHeapQueue

start_time = time.time()

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def djikstra(graph, source):
    dist = {v: math.inf for v in graph}
    prev = {v: None for v in graph}
    queue = list(graph.keys())

    dist[source] = 0

    while len(queue) > 0:
        cur = min(queue, key=lambda vert: dist[vert])
        queue.remove(cur)
        for neighbor in graph[cur]:
            alt = dist[cur] + graph[cur][neighbor]
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = cur
    return dist, prev


def djikstra_minheap(graph, source):
    global start_time
    dist = {v: math.inf for v in graph}
    prev = {v: None for v in graph}
    queue = [source] + list(k for k in graph.keys() if k != source)

    dist[source] = 0

    while len(queue) > 0:
        if len(queue) % 1000 == 0:
            print(str(len(queue)) + "--- %s seconds ---" %
                  (time.time() - start_time))
            start_time = time.time()
        cur = queue.pop(0)
        for neighbor in graph[cur]:
            alt = dist[cur] + graph[cur][neighbor]
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                queue.remove(neighbor)
                for i in range(len(queue)):
                    vert = queue[i]
                    if dist[vert] > dist[neighbor]:
                        queue.insert(i, neighbor)
                        break
                prev[neighbor] = cur
    return dist, prev


def djikstra_custom_minheap(graph, source):
    global start_time
    dist = {v: math.inf for v in graph}
    prev = {v: None for v in graph}
    queue = MinHeapQueue()
    for vert in graph.keys():
        queue.push(vert, math.inf)
    queue.push(source, 0)

    dist[source] = 0

    while len(queue) > 0:
        if len(queue) % 1000 == 0:
            print(str(len(queue)), "--- %s seconds ---" %
                  (time.time() - start_time), queue.prio_len())
            start_time = time.time()
        cur = queue.pop()
        for neighbor in graph[cur]:
            alt = dist[cur] + graph[cur][neighbor]
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                queue.reprio(neighbor, dist[neighbor])
                prev[neighbor] = cur
    return dist, prev


def is_path_valid(path):
    dirs = list(tuple(map(lambda i, j: j - i, p1, p2))
                for p1, p2 in zip(path[:-1], path[1:]))
    repeats = (sum(1 for _ in g) for _, g in groupby(dirs))
    for repeat in repeats:
        if repeat > 3:
            return False
    return True


def get_path(prev, dest):
    path = []
    cur = dest
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))


def get_vertex_neighbors(vert_from, grid):
    neighbors = []
    for dir in DIRS:
        opposite_dir = (-dir[0], -dir[1])
        if vert_from[2] != opposite_dir:
            to = tuple(map(lambda i, j: i + j, vert_from[:2], dir))
            if to[0] >= 0 and to[1] >= 0 and to[0] < len(grid[0]) and to[1] < len(grid):
                if dir != vert_from[2]:
                    if to == (len(grid[0]) - 1, len(grid) - 1):
                        neighbors.append(to)
                    else:
                        neighbors.append((to[0], to[1], dir, 0))
                elif vert_from[3] + 1 < 3:
                    if to == (len(grid[0]) - 1, len(grid) - 1):
                        neighbors.append(to)
                    else:
                        neighbors.append((to[0], to[1], dir, vert_from[3] + 1))
    return neighbors


def build_graph(grid):
    vertex = []
    for j in range(len(grid)):
        for i in range(len(grid[j])):
            for dir in DIRS:
                for dist in range(3):
                    _from = tuple(
                        map(lambda a, b: a - b * (dist + 1), (i, j), dir))
                    if _from[0] >= 0 and _from[1] >= 0 and _from[0] < len(grid[0]) and _from[1] < len(grid):
                        vertex.append((i, j, dir, dist))
    graph = {vert: {} for vert in vertex}
    for vert_from in vertex:
        for vert_to in get_vertex_neighbors(vert_from, grid):
            graph[vert_from][vert_to] = grid[vert_to[1]][vert_to[0]]
    graph[(0, 0)] = {}
    graph[(0, 0)][(1, 0, (1, 0), 0)] = grid[0][1]
    graph[(0, 0)][(0, 1, (0, 1), 0)] = grid[1][0]
    graph[(len(grid[0]) - 1, len(grid) - 1)] = {}
    return graph


if __name__ == '__main__':
    f = open("input.txt", "r")

    grid = [[int(c) for c in line] for line in f.read().splitlines()]

    graph = build_graph(grid)
    print("Graph built")
    print(len(graph))

    dist, prev = djikstra_custom_minheap(graph, (0, 0))
    path = get_path(prev, (len(grid[0]) - 1, len(grid) - 1))
    print(path)

    for pos in path:
        grid[pos[1]][pos[0]] = "X"

    print(*("".join(str(c) for c in line) for line in grid), sep="\n")
    print(dist[(len(grid[0]) - 1, len(grid) - 1)])
