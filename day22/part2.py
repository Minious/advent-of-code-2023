import json
import copy
import os.path


def falling_blocks_count_when_desintegrating(block, blocks):
    _blocks = [_block for _block in copy.deepcopy(blocks) if _block != block]
    blocks_dropped = set()
    any_block_dropped = True
    while any_block_dropped:
        _blocks_dropped = drop_blocks(_blocks)
        blocks_dropped.update(block["name"] for block in _blocks_dropped)
        if len(_blocks_dropped) == 0:
            any_block_dropped = False
    return len(blocks_dropped)


def parse_block(line, name):
    _from = tuple(int(x) for x in line.split("~")[0].split(","))
    _to = tuple(int(x) for x in line.split("~")[1].split(","))
    return {"from": _from, "to": _to, "name": name}


def block_to_cubes(block):
    cubes = []
    for x in range(block["from"][0], block["to"][0] + 1):
        for y in range(block["from"][1], block["to"][1] + 1):
            for z in range(block["from"][2], block["to"][2] + 1):
                cubes.append((x, y, z))
    return cubes


def block_below(block, blocks):
    cubes = block_to_cubes(block)
    for other_block in blocks:
        if block != other_block:
            other_cubes = block_to_cubes(other_block)
            for cube in cubes:
                for other_cube in other_cubes:
                    if cube[0] == other_cube[0] and cube[1] == other_cube[1] and cube[2] == other_cube[2] + 1:
                        return True
    return False


def drop_blocks(blocks):
    # any_block_is_dropped = False
    dropped_blocks = []
    for block in sorted(blocks, key=lambda block: block["from"][2]):
        block_is_dropped = drop_block(block, blocks)
        if block_is_dropped:
            dropped_blocks.append(block)
    return dropped_blocks


def drop_block(block, blocks):
    if block["from"][2] == 1:
        return False
    if block_below(block, blocks):
        return False
    block["from"] = (block["from"][0], block["from"][1], block["from"][2] - 1)
    block["to"] = (block["to"][0], block["to"][1], block["to"][2] - 1)
    return True


def show_Xside_view(blocks, minX, maxX, minZ, maxZ):
    view = [["." for z in range(minZ, maxZ + 1)]
            for x in range(minX, maxX + 1)]
    for block in sorted(blocks, key=lambda block: -block["from"][1]):
        cubes = block_to_cubes(block)
        for cube in cubes:
            if view[cube[0]][cube[2] - 1] == ".":
                view[cube[0]][cube[2] - 1] = block["name"]
            elif view[cube[0]][cube[2] - 1] != block["name"]:
                view[cube[0]][cube[2] - 1] = "?"
    print(*(" ".join(str(x) for x in line)
          for line in reversed(list(zip(*view)))), sep="\n")
    print("- " * (maxX - minX + 1))


def show_Yside_view(blocks, minY, maxY, minZ, maxZ):
    view = [["." for z in range(minZ, maxZ + 1)]
            for y in range(minY, maxY + 1)]
    for block in sorted(blocks, key=lambda block: -block["from"][0]):
        cubes = block_to_cubes(block)
        for cube in cubes:
            if view[cube[1]][cube[2] - 1] == ".":
                view[cube[1]][cube[2] - 1] = block["name"]
            elif view[cube[1]][cube[2] - 1] != block["name"]:
                view[cube[1]][cube[2] - 1] = "?"
    print(*(" ".join(str(x) for x in line)
          for line in reversed(list(zip(*view)))), sep="\n")
    print("-" * (maxY - minY + 1))


if __name__ == '__main__':
    f = open("input_simple.txt", "r")

    blocks = [parse_block(line, chr(i))
              for i, line in enumerate(f.read().splitlines())]
    if os.path.isfile("blocks.txt"):
        with open("blocks.txt", "r") as fp:
            blocks = json.load(fp)
    minX = min(block["from"][0] for block in blocks)
    maxX = max(block["to"][0] for block in blocks)
    minY = min(block["from"][1] for block in blocks)
    maxY = max(block["to"][1] for block in blocks)
    print("X", minX, maxX)
    print("Y", minY, maxY)
    xy_to_block = [[[] for y in range(minY, maxY + 1)]
                   for x in range(minX, maxX + 1)]
    for block in blocks:
        cubes = block_to_cubes(block)
        for cube in cubes:
            xy_to_block[cube[0]][cube[1]].append(block)
    # for x in range(len(xy_to_block)):
    #     for y in range(len(xy_to_block[x])):
    #         blocks = xy_to_block[x][y]
    c = 0
    any_block_is_dropped = True
    while any_block_is_dropped:
        c += 1
        any_block_is_dropped = len(drop_blocks(blocks)) > 0
        print(c)
        with open("blocks.txt", "w") as fp:
            json.dump(blocks, fp)
    minZ = min(block["from"][2] for block in blocks)
    maxZ = max(block["to"][2] for block in blocks)
    print("Z", minZ, maxZ)
    show_Xside_view(blocks, minX, maxX, minZ, maxZ)
    show_Yside_view(blocks, minX, maxX, minZ, maxZ)

    # Brute force
    # s = 0
    # c = 0
    # for block in blocks:
    #     falling_blocks_count = falling_blocks_count_when_desintegrating(
    #         block, blocks)
    #     s += falling_blocks_count
    #     c += 1
    #     print("Iteration", c, ": Block",
    #           block["name"], s, "  +", falling_blocks_count)
    # print(s)

    block_to_supported_by = {block["name"]: set() for block in blocks}
    block_to_supporting = {block["name"]: set() for block in blocks}
    for block in blocks:
        cubes = block_to_cubes(block)
        for other_block in blocks:
            if block != other_block:
                other_block_supporting_block = False
                other_cubes = block_to_cubes(other_block)
                for cube in cubes:
                    for other_cube in other_cubes:
                        if cube[0] == other_cube[0] and cube[1] == other_cube[1] and cube[2] == other_cube[2] + 1:
                            other_block_supporting_block = True
                if other_block_supporting_block:
                    block_to_supported_by[block["name"]].add(
                        other_block["name"])
                    block_to_supporting[other_block["name"]].add(block["name"])

    s = 0
    for block in blocks:
        blocks_to_check = [block["name"]]
        blocks_falling = set(block["name"])
        while len(blocks_to_check) > 0:
            block_to_check = blocks_to_check.pop(0)
            for block_supported in block_to_supporting[block_to_check]:
                blocks_to_check.append(block_supported)
                if set(block_to_supported_by[block_supported]).issubset(blocks_falling):
                    blocks_falling.add(block_supported)
        s += len(blocks_falling) - 1
    print(s)
