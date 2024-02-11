def hash(s):
    r = 0
    for c in s:
        r += ord(c)
        r *= 17
        r %= 256
    return r


f = open("input.txt", "r")

boxes = [[] for _ in range(256)]
for instruction in f.read().split(","):
    if "=" in instruction:
        label, lens = instruction[:-2], int(instruction[-1])
        box_idx = hash(label)
        if label in [lens[0] for lens in boxes[box_idx]]:
            existing_lens_idx = [lens[0]
                                 for lens in boxes[box_idx]].index(label)
            boxes[box_idx][existing_lens_idx] = (label, lens)
        else:
            boxes[box_idx].append((label, lens))
    elif "-" in instruction:
        label = instruction[:-1]
        box_idx = hash(label)
        boxes[box_idx] = [lens for lens in boxes[box_idx] if lens[0] != label]

print(sum((box_idx + 1) * (lens_idx + 1) * lens[1] for box_idx, box in enumerate(boxes)
      for lens_idx, lens in enumerate(box)))
