f = open("input.txt", "r")

grid = [[int(c) for c in line] for line in f.read().splitlines()]


colors = {
    "0": '\033[48;5;34m',
    "1": '\033[48;5;70m',
    "2": '\033[48;5;106m',
    "3": '\033[48;5;142m',
    "4": '\033[48;5;178m',
    "5": '\033[48;5;214m',
    "6": '\033[48;5;215m',
    "7": '\033[48;5;216m',
    "8": '\033[48;5;218m',
    "9": '\033[48;5;219m',
    "ENDC": '\033[0m'
}


print(
    *("".join((f"{colors[str(c)]} {colors['ENDC']}" for c in line)) for line in grid), sep="\n")
