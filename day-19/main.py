from functools import partial
from pathlib import Path


def parse_parts(filename: str) -> list[dict]:
    lines = Path(filename).read_text().splitlines()

    result = []

    for line in lines:
        part = {}

        for assignment in line[1:-1].split(","):
            key, value = assignment.split("=")
            part[key] = int(value)

        result.append(part)

    return result


def evaluate_condition(
    property: str, operator: str, threshold: int, part: dict
) -> bool:
    if operator == ">":
        return part[property] > threshold
    if operator == "<":
        return part[property] < threshold
    raise ValueError(f"Unexpected operator '{operator}'")


def always_true(_part: dict) -> bool:
    return True


def parse_workflows(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()

    result = {}

    for line in lines:
        name, rules = line[:-1].split("{")

        rules_list = []
        for rule in rules.split(","):
            if ":" not in rule:
                rules_list.append(
                    {"condition": None, "condition_func": always_true, "target": rule}
                )
            else:
                condition_text, target = rule.split(":")
                property, operator, threshold = (
                    condition_text[0],
                    condition_text[1],
                    int(condition_text[2:]),
                )
                rules_list.append(
                    {
                        "condition": {
                            "property": property,
                            "operator": operator,
                            "threshold": threshold,
                        },
                        "condition_func": partial(
                            evaluate_condition, property, operator, threshold
                        ),
                        "target": target,
                    }
                )

        result[name] = rules_list

    return result


def evaluate_workflow(workflow: list, part: dict) -> str:
    for rule in workflow:
        if rule["condition_func"](part):
            return rule["target"]

    raise ValueError("Workflow did not apply to part")


def part_1():
    parts = parse_parts("parts.txt")
    workflows = parse_workflows("workflows.txt")

    accepted_parts = []

    for part in parts:
        current_stage = "in"

        while current_stage not in {"A", "R"}:
            workflow = workflows[current_stage]
            current_stage = evaluate_workflow(workflow, part)

        if current_stage == "A":
            accepted_parts.append(part)


    return sum(sum(part.values()) for part in accepted_parts)


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
