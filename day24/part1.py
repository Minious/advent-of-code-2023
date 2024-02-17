def parse_hailstone(line):
    line = "".join(c for c in line if c != " ")
    return {"pos": tuple(int(x) for x in line.split("@")[0].split(",")), "vel": tuple(int(x) for x in line.split("@")[1].split(","))}


def rays_intersect(r1, r2):
    dx = r2["pos"][0] - r1["pos"][0]
    dy = r2["pos"][1] - r1["pos"][1]
    det = r2["vel"][0] * r1["vel"][1] - r2["vel"][1] * r1["vel"][0]
    if det == 0:
        return False, 0, 0
    u = (dy * r2["vel"][0] - dx * r2["vel"][1]) / det
    v = (dy * r1["vel"][0] - dx * r1["vel"][1]) / det
    return u > 0 and v > 0, u, v


if __name__ == '__main__':
    f = open("input.txt", "r")

    hailstones = [parse_hailstone(line) for line in f.read().splitlines()]

    bounds = (200000000000000, 400000000000000)
    intersections_count = 0
    for i, r1 in enumerate(hailstones):
        for r2 in hailstones[i + 1:]:
            intersect, u, v = rays_intersect(r1, r2)
            if intersect:
                p = (r1["pos"][0] + r1["vel"][0] * u,
                     r1["pos"][1] + r1["vel"][1] * u)
                if p[0] >= bounds[0] and p[1] >= bounds[0] and p[0] < bounds[1] and p[1] < bounds[1]:
                    # print("Intersection", r1, r2)
                    intersections_count += 1
    print(intersections_count)
