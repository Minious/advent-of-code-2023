import time


def parse_condition(condition_str):
    if ">" in condition_str:
        return {"property": condition_str.split(">")[0], "value": int(condition_str.split(">")[1]), "operator": ">"}
    if "<" in condition_str:
        return {"property": condition_str.split("<")[0], "value": int(condition_str.split("<")[1]), "operator": "<"}


def parse_workflows(workflows_str):
    workflows = {}
    for workflow_str in workflows_str:
        workflow_name = workflow_str.split("{")[0]
        instructions = workflow_str.split("{")[1][:-1].split(",")
        instructions = [{"condition": parse_condition(instruction.split(
            ":")[0]), "destination": instruction.split(
            ":")[1]} for instruction in instructions[:-1]] + [{"condition": "True", "destination": instructions[-1]}]
        workflows[workflow_name] = instructions
    return workflows


def get_base_ranges():
    return {
        "x": {"min": 1, "max": 4000},
        "m": {"min": 1, "max": 4000},
        "a": {"min": 1, "max": 4000},
        "s": {"min": 1, "max": 4000},
    }


def apply_condition(_ranges, condition, valid=True):
    ranges = {k: {l: w for l, w in v.items()} for k, v in _ranges.items()}
    if condition["operator"] == ">" and valid:
        ranges[condition["property"]]["min"] = max(
            ranges[condition["property"]]["min"], condition["value"] + 1)
    if condition["operator"] == "<" and valid:
        ranges[condition["property"]]["max"] = min(
            ranges[condition["property"]]["max"], condition["value"] - 1)
    if condition["operator"] == ">" and not valid:
        ranges[condition["property"]]["max"] = min(
            ranges[condition["property"]]["max"], condition["value"])
    if condition["operator"] == "<" and not valid:
        ranges[condition["property"]]["min"] = max(
            ranges[condition["property"]]["min"], condition["value"])
    if ranges[condition["property"]]["min"] >= ranges[condition["property"]]["max"]:
        return None
    else:
        return ranges


def get_intervals2(els, property):
    bounds = sorted(set([1, 4000] + [el["ranges"][property]["min"] for el in done] + [el["ranges"][property]["min"] -
                                                                                      1 for el in done] + [el["ranges"][property]["max"] + 1 for el in done] + [el["ranges"][property]["max"] for el in els]))
    bounds.remove(0)
    bounds.remove(4001)
    intervals = []
    for i, bound in enumerate(bounds[:-1]):
        intervals.append((bound, bound))
        next_bound = bounds[i + 1]
        if bound != next_bound - 1:
            intervals.append((bound + 1, next_bound - 1))
    return intervals


def get_intervals(els, property):
    bounds = sorted(set([(1, "min"), (4000, "max")] + [(el["ranges"][property]["min"], "min")
                    for el in done] + [(el["ranges"][property]["max"], "max") for el in els]))
    intervals = []
    for x, y in zip(bounds[:-1], bounds[1:]):
        _min = x[0] if x[1] == "min" else x[0] + 1
        _max = y[0] if y[1] == "max" else y[0] - 1
        if _min < _max:
            intervals.append((_min, _max))
    return intervals


def fits(el, x_interval, m_interval, a_interval, s_interval):
    return (x_interval[0] >= el["x"]["min"] and x_interval[1] <= el["x"]["max"] and
            m_interval[0] >= el["m"]["min"] and m_interval[1] <= el["m"]["max"] and
            a_interval[0] >= el["a"]["min"] and a_interval[1] <= el["a"]["max"] and
            s_interval[0] >= el["s"]["min"] and s_interval[1] <= el["s"]["max"])


def get_ranges_width(ranges):
    return -sum(range["max"] - range["min"] + 1 for range in ranges.values())


def is_range_in_range(r_out, r_in):
    return (r_in["x"]["min"] >= r_out["x"]["min"] and r_in["x"]["max"] <= r_out["x"]["max"] and
            r_in["m"]["min"] >= r_out["m"]["min"] and r_in["m"]["max"] <= r_out["m"]["max"] and
            r_in["a"]["min"] >= r_out["a"]["min"] and r_in["a"]["max"] <= r_out["a"]["max"] and
            r_in["s"]["min"] >= r_out["s"]["min"] and r_in["s"]["max"] <= r_out["s"]["max"])


if __name__ == '__main__':
    f = open("input.txt", "r")

    lines = f.read().splitlines()

    empty_line_idx = lines.index("")
    workflows_str = lines[:empty_line_idx]
    workflows = parse_workflows(workflows_str)

    queue = [{"ranges": get_base_ranges(), "workflow": "in", "step": 0}]
    done = []
    while len(queue) > 0:
        el = queue.pop()
        if el["workflow"] == "A":
            done.append(el)
            continue
        elif el["workflow"] == "R":
            continue
        workflow = workflows[el["workflow"]]
        instruction = workflow[el["step"]]
        if instruction["condition"] == "True":
            el["workflow"] = instruction["destination"]
            el["step"] = 0
            queue.append(el)
        else:
            condition = instruction["condition"]
            new_ranges_valid = apply_condition(el["ranges"], condition)
            if new_ranges_valid != None:
                queue.append({"ranges": new_ranges_valid,
                             "workflow": instruction["destination"], "step": 0})
            new_ranges_invalid = apply_condition(
                el["ranges"], condition, False)
            if new_ranges_invalid != None:
                queue.append({"ranges": new_ranges_invalid,
                             "workflow": el["workflow"], "step": el["step"] + 1})

    print("Sorting....")
    done = sorted(done, key=lambda a: get_ranges_width(a["ranges"]))
    print("Sorted !")
    # print(*done, sep="\n")

    # OMG la réponse était si simple j'y ai passé des heures la prépa ça date de fou
    s = 0
    for el in done:
        c = 1
        for property in el["ranges"]:
            c *= el["ranges"][property]["max"] - \
                el["ranges"][property]["min"] + 1
        s += c
    print("CHATTE", s)

    # Toute la suite sert à rien
    for el1 in done:
        for el2 in done:
            if el1 != el2:
                if is_range_in_range(el1["ranges"], el2["ranges"]):
                    print("prout")

    x_intervals = get_intervals(done, "x")
    m_intervals = get_intervals(done, "m")
    a_intervals = get_intervals(done, "a")
    s_intervals = get_intervals(done, "s")

    comb = len(x_intervals) * len(m_intervals) * \
        len(a_intervals) * len(s_intervals)
    print(comb)

    s = 0
    c = 0
    start_time = time.time()
    for x_interval in x_intervals:
        print("Round X", x_interval)
        for m_interval in m_intervals:
            print("Round M", m_interval)
            for a_interval in a_intervals:
                for s_interval in s_intervals:
                    c += 1
                    if c % 100000 == 0:
                        # print(str(c).rjust(len(str(comb))))
                        print("{:.3%}".format(c/comb),
                              "{:.3f}s".format(time.time() - start_time))
                    for el in done:
                        if fits(el["ranges"], x_interval, m_interval, a_interval, s_interval):
                            # print(x_interval, m_interval, a_interval,
                            #       s_interval, "fits in", el)
                            s += (x_interval[1] - x_interval[0] + 1)*(m_interval[1] - m_interval[0] + 1)*(
                                a_interval[1] - a_interval[0] + 1)*(s_interval[1] - s_interval[0] + 1)
                            break
    print(s)
