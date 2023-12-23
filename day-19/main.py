from collections import deque
from dataclasses import dataclass, replace
from functools import partial
from pathlib import Path
from typing import Optional


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


@dataclass
class Limits:
    x_min: int
    x_max: int

    m_min: int
    m_max: int

    a_min: int
    a_max: int

    s_min: int
    s_max: int

    def apply(self, condition: Optional[dict]) -> "Limits":
        if condition is None:
            return self

        copy = replace(self)

        property = condition["property"]
        operator = condition["operator"]
        threshold = condition["threshold"]

        if operator == "<":
            key = f"{property}_max"
            setattr(copy, key, min(getattr(copy, key), threshold - 1))
        elif operator == "<=":
            key = f"{property}_max"
            setattr(copy, key, min(getattr(copy, key), threshold))
        elif operator == ">":
            key = f"{property}_min"
            setattr(copy, key, max(getattr(copy, key), threshold + 1))
        elif operator == ">=":
            key = f"{property}_min"
            setattr(copy, key, max(getattr(copy, key), threshold))
        else:
            raise ValueError(f"Unexpected operator '{operator}'")

        return copy

    def inverse_apply(self, condition: Optional[dict]) -> "Limits":
        if condition is None:
            return self

        property = condition["property"]
        operator = condition["operator"]
        threshold = condition["threshold"]

        inverse_operator = {"<": ">=", "<=": ">", ">": "<=", ">=": "<"}[operator]

        return self.apply(
            {"property": property, "operator": inverse_operator, "threshold": threshold}
        )

    def count(self) -> int:
        x_count = max(self.x_max - self.x_min + 1, 0)
        m_count = max(self.m_max - self.m_min + 1, 0)
        a_count = max(self.a_max - self.a_min + 1, 0)
        s_count = max(self.s_max - self.s_min + 1, 0)

        return x_count * m_count * a_count * s_count


def part_2():
    # The workflow graph is a tree
    # We do a depth-first traversal, adding a Limits object to each node
    # This object represents the limits of the parts that can reach this node
    # When we reach a node that is an accept state, we collect the appropriate Limits object into a list
    # The result is the sum of the counts of all the Limits objects in the list

    workflows = parse_workflows("workflows.txt")

    initial_limits = Limits(1, 4000, 1, 4000, 1, 4000, 1, 4000)

    queue = deque([("in", initial_limits)])

    succesful_limits = []

    while len(queue) > 0:
        current_stage, limits = queue.popleft()

        workflow = workflows[current_stage]

        for rule in workflow:
            if rule["target"] == "A":
                succesful_limits.append(limits.apply(rule["condition"]))
            elif rule["target"] == "R":
                pass
            else:
                queue.append((rule["target"], limits.apply(rule["condition"])))

            # Each workflow can have many rules, and for the nth rule to apply,
            # all of the conditions of the previous rules must not apply.
            # To handle that we apply the inverse of the current condition at the end of each step
            # as we loop through the rules of the workflow.
            limits = limits.inverse_apply(rule["condition"])

    return sum(limit.count() for limit in succesful_limits)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
