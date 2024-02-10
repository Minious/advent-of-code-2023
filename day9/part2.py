import re

f = open("input.txt", "r")

lines = f.read().splitlines()


def get_next_step(step):
    return [m - n for n, m in zip(step[:-1], step[1:])]


def get_all_steps(step):
    steps = [step]
    while len(steps[-1]) > 1:
        steps.append(get_next_step(steps[-1]))
    return steps


def extrapolate_steps(steps):
    steps.append([0])
    for i in range(len(steps) - 2, -1, -1):
        current_step = steps[i]
        next_step = steps[i + 1]
        current_step.insert(0, current_step[0] - next_step[0])


list_steps = []
for line in lines:
    step = [int(x) for x in line.split(" ")]
    steps = get_all_steps(step)
    print(*steps, sep="\n")
    extrapolate_steps(steps)
    print(*steps, sep="\n")
    list_steps.append(steps)

print(sum(steps[0][0] for steps in list_steps))
