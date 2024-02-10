import re
import functools


def to_graphviz(nodes):
    with open("output.txt", "w") as ml:
        for node in nodes:
            ml.write(node + " -> " + nodes[node][0]+"[color=\"red\"]\n")
            ml.write(node + " -> " + nodes[node][1]+"[color=\"blue\"]\n")


def to_graphviz_Z(nodes):
    cur_nodes = [(node, 0) for node in nodes if node.endswith("Z")]
    processed_nodes = [(node, 0) for node in nodes if node.endswith("Z")]
    with open("output_z.txt", "w") as ml:
        while len(cur_nodes) > 0:
            node = cur_nodes[0][0]
            for child_node in nodes:
                if node in nodes[child_node]:
                    if child_node not in (x[0] for x in cur_nodes) and child_node not in processed_nodes and cur_nodes[0][1] < 10:
                        cur_nodes.append((child_node, cur_nodes[0][1] + 1))
                    ml.write(child_node + " -> " + node +
                             "[color=\"" + ("red" if node == nodes[child_node][0] else "blue") + "\"]" + "\n")
            cur_nodes.pop(0)
            processed_nodes.append(node)


def get_loop_count(node, nodes):
    starting_node = node
    c = 0
    while nodes[node][0] != starting_node and nodes[node][1] != starting_node:
        node = nodes[node][0]
        c += 1
    return c + 1


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


f = open("input.txt", "r")

lines = f.read().splitlines()

instructions = lines[0]
print("Instructions count", len(instructions))
nodes = {t[0]: (t[1], t[2]) for t in (re.search(
    "([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line).groups() for line in lines[2:])}
cur_nodes = [node for node in nodes if node.endswith("A")]
n = [get_loop_count(nodes[node][0], nodes) for node in cur_nodes]

# _lcm = int(lcm(n))
# print(n)
# print(_lcm)

# i = 0
# last_instruction_idx = (_lcm * i) % len(instructions)
# while not instructions[:last_instruction_idx+1].endswith("RRRR"):
#     i += 1
#     last_instruction_idx = (_lcm * i) % len(instructions)
# print("WRONG ANSWER (for some reason)", _lcm * i)

# to_graphviz(nodes)
# to_graphviz_Z(nodes)

print("ANSWER", int(lcm(n + [len(instructions)])))
