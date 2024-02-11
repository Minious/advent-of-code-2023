def is_line_matching_template(line, template):
    groups_lengths = tuple(len(group)
                           for group in line.split(".") if group != "")
    return groups_lengths == template


def can_line_match_template(line, template):
    groups_lengths = [len(c) for c in line.split(".") if c != ""]
    _template = list(template)
    while len(groups_lengths) > 0 and len(_template) > 0:
        if _template[0] <= groups_lengths[0]:
            groups_lengths[0] -= _template[0] + 1
            _template.pop(0)
            if groups_lengths[0] <= 0:
                groups_lengths.pop(0)
        else:
            groups_lengths.pop(0)
    return len(_template) == 0


def nb_arrangements(line, template):
    if "?" not in line:
        return 1 if is_line_matching_template(line, template) else 0
    elif can_line_match_template(line, template):
        return nb_arrangements(line.replace("?", ".", 1), template) + nb_arrangements(line.replace("?", "#", 1), template)
    return 0


f = open("input.txt", "r")

lines = f.read().splitlines()

count = 0
i = 0
for _line in lines:
    print(i)
    line, template = _line.split(" ")
    template = tuple(int(x) for x in template.split(","))
    count += nb_arrangements(line, template)
    i += 1
print(count)
