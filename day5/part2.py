import re
import functools

f = open("input.txt", "r")


def fill_range(_range):
    res = []
    for i in range(len(_range)-1):
        p = _range[i]
        n = _range[i+1]
        res.append(p)
        if p["from"][1] < n["from"][0] - 1:
            new_range = (p["from"][1] + 1, n["from"][0] - 1)
            res.append({"from": new_range, "to": new_range})
    res.append(_range[-1])
    return res


def prepare_almanac(almanac):
    ret = {}
    for label in list(almanac.keys()):
        r = []
        for n in almanac[label]["ranges"]:
            r.append({"from": (n[1], n[1]+n[2]-1), "to": (n[0], n[0]+n[2]-1)})
        r.sort(key=lambda x: x["from"][0])
        r = fill_range(r)
        ret[label] = {"dest": almanac[label]["dest"], "ranges": r}
    return ret


def squash_almanac(almanac):
    while len(almanac) > 1:
        label = "seed"
        if almanac[label]["dest"] in almanac:
            c = almanac[label]
            n = almanac[almanac[label]["dest"]]
            thresholds = [x["to"][0] for x in c["ranges"]] + \
                [x["from"][0] for x in n["ranges"]]
            thresholds.sort()
            for threshold in thresholds:
                c["ranges"] = cut_ranges(c["ranges"], threshold, "to")
                n["ranges"] = cut_ranges(n["ranges"], threshold, "from")
            squashed_ranges = squash_ranges(c["ranges"], n["ranges"])
            del almanac[almanac[label]["dest"]]
            almanac[label] = {"dest": n["dest"], "ranges": squashed_ranges}


def squash_ranges(c, n):
    ret = []
    for _range_c in c:
        t = True
        for _range_n in n:
            if _range_c["to"] == _range_n["from"]:
                ret.append({"from": _range_c["from"], "to": _range_n["to"]})
                t = False
                break
        if t:
            print("FUCK")
    return ret


def cut_ranges(ranges, threshold, dest):
    ret = []
    for _range in ranges:
        if _range[dest][0] < threshold and threshold < _range[dest][1]:
            threshold_from = threshold if dest == "from" else threshold - \
                _range["to"][0] + _range["from"][0]
            threshold_to = threshold if dest == "to" else threshold - \
                _range["from"][0] + _range["to"][0]
            ret.append(
                {"from": (_range["from"][0], threshold_from - 1), "to": (_range["to"][0], threshold_to - 1)})
            ret.append({"from": (threshold_from, _range["from"][1]), "to": (
                threshold_to, _range["to"][1])})
        else:
            ret.append(_range)
    return ret


def convert(state, label, almanac):
    ranges = almanac[label]["ranges"]
    for _range in ranges:
        if state >= _range[1] and state < _range[1] + _range[2]:
            return state - _range[1] + _range[0]
    return state


lines = [line[:-1] for line in list(f)]

almanac = {}

first_line = [int(n) for n in lines[0].split(" ")[1:]]
seeds = [(m, n+m-1) for m, n in zip(first_line[0::2], first_line[1::2])]
chunks = re.findall("[a-z]+-to-[a-z]+ map:[0-9 ,]+", ",".join(lines))
for chunk in chunks:
    labels = re.search("[a-z]+-to-[a-z]+", chunk).group().split("-to-")
    ranges = [[int(n) for n in r.split(" ")]
              for r in chunk.split(",")[1:] if r != ""]
    almanac[labels[0]] = {"dest": labels[1], "ranges": ranges}

almanac = prepare_almanac(almanac)
squash_almanac(almanac)
seeds.sort(key=lambda a: a[0])

best = None
gne = 0
for seed in seeds:
    for _range in almanac[list(almanac.keys())[0]]["ranges"]:
        if _range["from"][0] <= seed[1] and seed[0] <= _range["from"][1]:
            _min = max(_range["from"][0], seed[0])
            _max = min(_range["from"][1], seed[1])
            location = _min - _range["from"][0] + _range["to"][0]
            if best == None or best > location:
                best = location
                gne = _min
print("OMG it worked", best)
