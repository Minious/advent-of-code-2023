import re

f = open("input.txt", "r")


def convert(state, label, almanac):
    ranges = almanac[label]["ranges"]
    for _range in ranges:
        if state >= _range[1] and state < _range[1] + _range[2]:
            return state - _range[1] + _range[0]
    return state


lines = [line[:-1] for line in list(f)]

almanac = {}

seeds = [int(n) for n in lines[0].split(" ")[1:]]
chunks = re.findall("[a-z]+-to-[a-z]+ map:[0-9 ,]+", ",".join(lines))
for chunk in chunks:
    labels = re.search("[a-z]+-to-[a-z]+", chunk).group().split("-to-")
    ranges = [[int(n) for n in r.split(" ")]
              for r in chunk.split(",")[1:] if r != ""]
    almanac[labels[0]] = {"dest": labels[1], "ranges": ranges}

current_label = "seed"
current_state = {current_label: seeds}
while current_label != "location":
    new_state = []
    new_label = almanac[current_label]["dest"]
    for state in current_state[current_label]:
        new_state.append(convert(state, current_label, almanac))
    current_state[new_label] = new_state
    current_label = new_label

print(min(current_state["location"]))
