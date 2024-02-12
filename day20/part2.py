import functools


def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a if b == 0 else b


def lcm(n):
    def rec(a, b):
        return a * b / gcd(a, b)
    return functools.reduce(lambda a, b: rec(a, b), n, 1)


if __name__ == '__main__':
    f = open("input.txt", "r")

    lines = f.read().splitlines()

    modules = {(line.split(" -> ")[0][1:] if line.split(" -> ")[0] != "broadcaster" else line.split(" -> ")[0]): {"type": line.split(" -> ")[0][0], "dest": line.split(" -> ")[1].split(", ")}
               for line in lines}
    # modules["button"] = {"type": "b", "dest": ["broadcaster"]}
    print(modules)

    flipflops = {k: False for k, v in modules.items() if v["type"] == "%"}
    print(flipflops)
    conjunctions = {k: {l: "low" for l, w in modules.items() if k in w["dest"]}
                    for k, v in modules.items() if v["type"] == "&"}
    print(conjunctions)

    done = False
    i = 0
    rem = {}
    interesting_modules = ["rl", "nn", "rd", "qb"]
    while len(interesting_modules) > len(rem):
        i += 1
        if i % 1000 == 0:
            print("Run", i)
        signals = [("broadcaster", "low", "button")]
        # print("button -low-> broadcaster")
        while len(signals) > 0:
            _from, signal_type, prev = signals.pop(0)
            if prev in interesting_modules and signal_type == "low" and prev not in rem:
                # print(prev, "broadcasted low on step", i)
                rem[prev] = i
            if _from == "rx" and signal_type == "low":
                done = True
                break
            if _from in modules:
                module = modules[_from]
            else:
                module = {"type": "X", "dest": []}
            match module["type"]:
                case "b":
                    for dest in module["dest"]:
                        # print(_from, "-"+signal_type+"->", dest)
                        signals.append((dest, signal_type, _from))
                case "%":
                    if signal_type == "high":
                        pass
                    elif signal_type == "low":
                        for dest in module["dest"]:
                            sent_signal_type = "low" if flipflops[_from] else "high"
                            # print(_from, "-"+sent_signal_type+"->", dest)
                            signals.append((dest, sent_signal_type, _from))
                        flipflops[_from] = not flipflops[_from]
                case "&":
                    conjunctions[_from][prev] = signal_type
                    sent_signal_type = "low" if all(
                        conjunctions[_from][prev] == "high" for prev in conjunctions[_from]) else "high"
                    for dest in module["dest"]:
                        # print(_from, "-"+sent_signal_type+"->", dest)
                        signals.append((dest, sent_signal_type, _from))
    print(int(lcm(rem.values())))
