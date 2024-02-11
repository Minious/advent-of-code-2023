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

# patterns = lines.split("")
blocks = [list(list(c for c in line) for line in block.split("\n"))
          for block in lines.split("\n\n")]

# print(*("\n".join(block) for block in blocks), sep="\n")

c = 0
for block in blocks:
    hor = [is_split_hor(block, i) for i in range(1, len(block))]
    if True in hor:
        print("Hor", hor.index(True) + 1)
        c += 100 * (hor.index(True) + 1)
    else:
        vert = [is_split_vert(block, i)
                for i in range(1, len(block[0]))]
        print("Vert", vert.index(True) + 1)
        c += vert.index(True) + 1
print(c)
