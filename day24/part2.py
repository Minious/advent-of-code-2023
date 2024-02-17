import math


def parse_hailstone(line):
    line = "".join(c for c in line if c != " ")
    return {"pos": tuple(int(x) for x in line.split("@")[0].split(",")), "vel": tuple(int(x) for x in line.split("@")[1].split(","))}


def hailstone_pos_at_time(initial_pos, vel, t):
    return tuple(map(lambda i, j: i + j * t, initial_pos, vel))


def cross_product(v1, v2):
    return (v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0])


def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


def diff(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])


def length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def distance_betweeen_lines(l1, l2):
    p1 = l1["pos"]
    p2 = l2["pos"]
    v1 = l1["vel"]
    v2 = l2["vel"]
    vel_cross = cross_product(v1, v2)
    return abs(dot(diff(p2, p1), vel_cross)) / length(vel_cross)


def div(v, d):
    return (v[0] / d, v[1] / d, v[2] / d)


def mult(v, m):
    return (v[0] * m, v[1] * m, v[2] * m)


def get_stone_bruteforce(hailstones, max_t):
    best = None
    for t1 in range(max_t + 1):
        for t2 in range(max_t + 1):
            p1 = hailstone_pos_at_time(
                hailstones[0]["pos"], hailstones[0]["vel"], t1)
            p2 = hailstone_pos_at_time(
                hailstones[1]["pos"], hailstones[1]["vel"], t2)
            stone = {"pos": p1, "vel": diff(p2, p1)}
            d = list(distance_betweeen_lines(stone, hailstone)
                     for hailstone in hailstones[2:])

            e = math.sqrt(sum(x*x for x in d))
            if best == None or e < best["e"]:
                best = {"e": e, "d": d, "p1": p1, "p2": p2, "t1": t1, "t2": t2}
    v0 = div(diff(best["p2"], best["p1"]), best["t2"] - best["t1"])
    p0 = diff(best["p1"], mult(v0, best["t1"]))
    return {"pos": p0, "vel": v0}, best


def get_stone(hailstones, min_t1, max_t1, min_t2, max_t2):
    best = None
    t1_range = max_t1 - min_t1
    t2_range = max_t2 - min_t2
    step1 = max(1, math.floor(t1_range / 100))
    step2 = max(1, math.floor(t2_range / 100))
    for t1 in range(min_t1, max_t1 + 1, step1):
        for t2 in range(min_t2, max_t2 + 1, step2):
            if t1 == t2:
                continue
            p1 = hailstone_pos_at_time(
                hailstones[0]["pos"], hailstones[0]["vel"], t1)
            p2 = hailstone_pos_at_time(
                hailstones[1]["pos"], hailstones[1]["vel"], t2)
            stone = {"pos": p1, "vel": diff(p2, p1)}
            d = list(distance_betweeen_lines(stone, hailstone)
                     for hailstone in hailstones[2:5])

            e = math.sqrt(sum(x*x for x in d))
            if best == None or e < best["e"]:
                best = {"e": e, "d": d, "p1": p1, "p2": p2, "t1": t1, "t2": t2}
    v0 = div(diff(best["p2"], best["p1"]), best["t2"] - best["t1"])
    p0 = diff(best["p1"], mult(v0, best["t1"]))
    return {"pos": p0, "vel": v0}, best


if __name__ == '__main__':
    f = open("input_less_simple.txt", "r")

    hailstones = [parse_hailstone(line) for line in f.read().splitlines()]

    max_t = 0
    for hailstone in hailstones:
        if hailstone["vel"][2] < 0:
            ground_hit_t = - \
                math.ceil(hailstone["pos"][2] / hailstone["vel"][2])
            if ground_hit_t > max_t:
                max_t = ground_hit_t

    min_t1 = 0
    max_t1 = max_t
    min_t2 = 0
    max_t2 = max_t
    stone, data = get_stone(hailstones, min_t1, max_t1, min_t2, max_t2)
    print(data)
    while data["e"] != 0:
        prev_t1_range = max_t1 - min_t1
        prev_t2_range = max_t2 - min_t2
        min_t1 = math.floor(data["t1"] - prev_t1_range / 100)
        max_t1 = math.ceil(data["t1"] + prev_t1_range / 100)
        min_t2 = math.floor(data["t2"] - prev_t2_range / 100)
        max_t2 = math.ceil(data["t2"] + prev_t2_range / 100)
        stone, data = get_stone(
            hailstones, min_t1, max_t1, min_t2, max_t2)
        print(data)
    print("Res", int(sum(stone["pos"])))
