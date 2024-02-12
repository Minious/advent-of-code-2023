if __name__ == '__main__':
    f = open("input.txt", "r")

    lines = f.read().splitlines()

    modules = {(line.split(" -> ")[0][1:] if line.split(" -> ")[0] != "broadcaster" else line.split(" -> ")[0]): {"type": line.split(" -> ")[0][0], "dest": line.split(" -> ")[1].split(", ")}
               for line in lines}

    w = open("output.txt", "w")
    for module in modules:
        color = "red" if modules[module]["type"] == "%" else "blue" if modules[module]["type"] == "&" else "green"
        w.write(module + ' [color="' + color + '"]\n')
        for dest in modules[module]["dest"]:
            w.write(module + " -> " + dest+"\n")
