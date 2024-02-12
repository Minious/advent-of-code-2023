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


def parse_parts(parts_str):
    parts = [line[1:-1].split(",") for line in lines[empty_line_idx + 1:]]
    parts = [{property.split("=")[0]: int(property.split("=")[1])
              for property in part} for part in parts]
    return parts


if __name__ == '__main__':
    f = open("input.txt", "r")

    lines = f.read().splitlines()

    empty_line_idx = lines.index("")
    workflows_str = lines[:empty_line_idx]
    parts_str = lines[empty_line_idx + 1:]
    # print(workflows_str)
    # print("====================")
    # print(parts_str)
    workflows = parse_workflows(workflows_str)
    parts = parse_parts(parts_str)

    s = 0
    for part in parts:
        step = "in"
        while step != "R" and step != "A":
            for instruction in workflows[step]:
                condition = instruction["condition"]
                destination = instruction["destination"]
                if instruction["condition"] == "True":
                    step = destination
                    break
                property = part[instruction["condition"]["property"]]
                if instruction["condition"]["operator"] == ">" and property > instruction["condition"]["value"] or instruction["condition"]["operator"] == "<" and property < instruction["condition"]["value"]:
                    step = destination
                    break
        if step == "A":
            s += sum(part.values())
print(s)
