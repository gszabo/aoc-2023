from pathlib import Path

import networkx as nx
from networkx.algorithms.connectivity import minimum_edge_cut


def parse_input(filename: str) -> nx.Graph:
    lines = Path(filename).read_text().splitlines()

    graph = nx.Graph()
    for line in lines:
        node, neighbours = list(map(str.strip, line.split(":")))
        neighbours = list(map(str.strip, neighbours.split(" ")))
        for neighbour in neighbours:
            graph.add_edge(node, neighbour)

    return graph


def part_1():
    graph = parse_input("input.txt")

    edges_to_cut = minimum_edge_cut(graph)
    assert len(edges_to_cut) == 3

    for u, v in edges_to_cut:
        graph.remove_edge(u, v)

    connected_component_sizes = [len(c) for c in nx.connected_components(graph)]
    assert len(connected_component_sizes) == 2

    return connected_component_sizes[0] * connected_component_sizes[1]


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
