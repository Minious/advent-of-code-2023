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

    low_count = 0
    high_count = 0
    for i in range(1000):
        print("Run", i)
        signals = [("broadcaster", "low", "button")]
        # print("button -low-> broadcaster")
        while len(signals) > 0:
            _from, signal_type, prev = signals.pop(0)
            if signal_type == "low":
                low_count += 1
            elif signal_type == "high":
                high_count += 1
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
    print("low", low_count, "high", high_count)
    print("answer", low_count * high_count)
