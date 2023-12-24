from collections import deque
from pathlib import Path


def parse_input(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()

    result = {}

    for line in lines:
        module, connections = line.split(" -> ")
        connections = [c.strip() for c in connections.split(",")]

        if module.startswith("%"):
            name = module[1:]
            result[name] = {"connections": connections, "type": "FF", "state": False}
        elif module.startswith("&"):
            name = module[1:]
            result[name] = {"connections": connections, "type": "CON", "state": {}}
        elif module == "broadcaster":
            result[module] = {"connections": connections, "type": "BROADCAST"}
        else:
            raise ValueError(f"Unknown module type: {module}")

    con_modules = [name for name, module in result.items() if module["type"] == "CON"]
    for name in con_modules:
        input_modules = [m for m in result if name in result[m]["connections"]]
        result[name]["state"] = {im: False for im in input_modules}

    result["button"] = {"connections": ["broadcaster"], "type": "BUTTON"}

    return result


def part_1():
    graph = parse_input("input.txt")

    low_signals = 0
    high_signals = 0

    for _ in range(1000):
        # implement signal propagation with a depth-first traversal
        queue = deque([("button", "broadcaster", False)])

        while len(queue) > 0:
            # popLEFT, silly github copilot generated it with pop, resulting in a wrong answer, but only for PART 2
            source, target, value = queue.popleft()

            if value is False:
                low_signals += 1
            else:
                high_signals += 1

            if target not in graph:
                continue

            type = graph[target]["type"]
            connections = graph[target]["connections"]
            state = graph[target].get("state")

            if type == "FF":
                if value is False:
                    new_state = not state
                    queue.extend([(target, c, new_state) for c in connections])
                    graph[target]["state"] = new_state
            elif type == "CON":
                state[source] = value
                # if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
                if all(state.values()):
                    queue.extend([(target, c, False) for c in connections])
                else:
                    queue.extend([(target, c, True) for c in connections])
            elif type == "BROADCAST":
                queue.extend([(target, c, value) for c in connections])
            elif type == "BUTTON":
                queue.extend([(target, c, False) for c in connections])
            else:
                raise ValueError(f"Unknown module type: {type}")

    return low_signals * high_signals


def part_2():
    graph = parse_input("input.txt")

    # fp, zc, xt, mk
    # bad_boys = ["fp", "zc", "xt", "mk"]

    for i in range(5000):
        queue = deque([("button", "broadcaster", False)])

        while len(queue) > 0:
            source, target, value = queue.popleft()

            if target == "kl" and value is True:
                print("kl received a high signal at", i + 1, "from", source)

            if target not in graph:
                continue

            type = graph[target]["type"]
            connections = graph[target]["connections"]
            state = graph[target].get("state")

            if type == "FF":
                if value is False:
                    new_state = not state
                    queue.extend([(target, c, new_state) for c in connections])
                    graph[target]["state"] = new_state
            elif type == "CON":
                state[source] = value

                # if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
                if all(state.values()):
                    queue.extend([(target, c, False) for c in connections])
                else:
                    queue.extend([(target, c, True) for c in connections])
            elif type == "BROADCAST":
                queue.extend([(target, c, value) for c in connections])
            elif type == "BUTTON":
                queue.extend([(target, c, False) for c in connections])
            else:
                raise ValueError(f"Unknown module type: {type}")

    # todo: multiply the printed values (or to be precise, find the least common multiple of them)


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
