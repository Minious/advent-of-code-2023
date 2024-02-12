DIR = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}


def get_neighbors(cur):
    return [tuple(map(lambda i, j: i + j, cur, dir)) for dir in DIR.values()]


def det(p1, p2):
    return p1[0] * p2[1] - p1[1] * p2[0]


def shoelace(polygon):
    a = 0
    for p1, p2 in zip(polygon, polygon[1:] + [polygon[0]]):
        a += det(p1, p2)
    return a / 2


if __name__ == '__main__':
    f = open("input.txt", "r")

    num_to_dir = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }

    instructions = [line.split(" ")[2][2:-1] for line in f.read().splitlines()]
    instructions = [(num_to_dir[instruction[-1]], int(instruction[:-1], 16))
                    for instruction in instructions]

    cur = (0, 0)
    polygon = []
    for i, instruction in enumerate(instructions):
        cur = tuple(map(lambda i, j: i + j *
                    int(instruction[1]), cur, DIR[instruction[0]]))
        next_instruction = instructions[(i + 1) % len(instructions)]
        offset = None
        match instruction[0]+next_instruction[0]:
            case "RU":
                offset = (-.5, -.5)
            case "RD":
                offset = (.5, -.5)
            case "LU":
                offset = (-.5, .5)
            case "LD":
                offset = (.5, .5)
            case "UL":
                offset = (-.5, .5)
            case "UR":
                offset = (-.5, -.5)
            case "DL":
                offset = (.5, .5)
            case "DR":
                offset = (.5, -.5)
            case _:
                print("BUG")
        point = tuple(map(lambda i, j: i + j, cur, offset))
        polygon.append(point)
    print(int(shoelace(polygon)))
