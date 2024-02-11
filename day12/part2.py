def nb_arrangements(line, template):
    memo = {}

    def rec(line, template):
        key = (line, template)
        if key in memo:
            return memo[key]
        if len(template) == 0:
            return 1 if "#" not in line else 0
        c = 0
        while len(template) - 1 + sum(template) <= len(line):
            if "." in line[:template[0]]:
                pass
            elif template[0] < len(line) and line[template[0]] == "#":
                pass
            else:
                a = rec(
                    line[template[0] + 1:], template[1:])
                c += a
            if line[0] == "#":
                break
            line = line[1:]
        memo[key] = c
        return c

    return rec(line, template)


f = open("input.txt", "r")

lines = f.read().splitlines()

count = 0
mult = 5
for _line in lines:
    line, template = _line.split(" ")
    line = "?".join([line] * mult)
    template = tuple(int(x) for x in template.split(",")) * mult
    count += nb_arrangements(line, template)
print(count)
