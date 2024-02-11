def is_split_hor(block, i):
    block1 = tuple(block[:i][::-1])
    block2 = tuple(block[i:])
    min_len = min(len(block1), len(block2))
    return block1[:min_len] == block2[:min_len]


def is_split_vert(block, i):
    block1 = tuple(list(zip(*block))[:i][::-1])
    block2 = tuple(list(zip(*block))[i:])
    min_len = min(len(block1), len(block2))
    return block1[:min_len] == block2[:min_len]


f = open("input.txt", "r")

lines = f.read()

blocks = [list(list(c for c in line) for line in block.split("\n"))
          for block in lines.split("\n\n")]


def find_mirrors(block):
    return [("hor", i)
            for i in range(1, len(block)) if is_split_hor(block, i)] + [("vert", i)
                                                                        for i in range(1, len(block[0])) if is_split_vert(block, i)]


def find_new_mirror(_block):
    prev = find_mirrors(_block)[0]
    for i in range(len(_block)):
        for j in range(len(_block[i])):
            block = [line[:] for line in _block]
            block[i][j] = "." if _block[i][j] == "#" else "#"
            cur = find_mirrors(block)
            if len(cur) >= 1:
                if prev in cur:
                    cur.remove(prev)
                if len(cur) == 1:
                    return cur[0]


c = 0
for _block in blocks:
    cur = find_new_mirror(_block)
    if cur == None:
        print("not found")
    elif cur[0] == "hor":
        print(cur)
        c += 100 * cur[1]
    elif cur[0] == "vert":
        print(cur)
        c += cur[1]
print(c)
