from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def visualize(filename: str):
    lines = Path(filename).read_text().splitlines()

    g = nx.DiGraph()

    color_map = {}

    for line in lines:
        module, connections = line.split(" -> ")
        connections = [c.strip() for c in connections.split(",")]

        module_name = module[1:] if module[0] in "&%" else module

        if module.startswith("%"):
            color_map[module_name] = "yellow"
        elif module.startswith("&"):
            color_map[module_name] = "green"
        elif module == "broadcaster":
            color_map[module_name] = "blue"

        for c in connections:
            g.add_edge(module_name, c)

    colors = [color_map.get(node, "violet") for node in g.nodes()]

    nx.draw(g, pos=graphviz_layout(g, prog="dot", root="rx"), with_labels=True, node_color=colors)
    plt.show()


if __name__ == "__main__":
    visualize("input.txt")
