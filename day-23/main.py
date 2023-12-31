from collections import defaultdict, deque
from pathlib import Path

Coord = tuple[int, int]


def parse_input(filename: str) -> dict:
    lines = Path(filename).read_text().splitlines()
    width = len(lines[0])
    height = len(lines)

    field = {}

    for y in range(height):
        for x in range(width):
            field[(x, y)] = lines[y][x]

    start = (lines[0].index("."), 0)
    end = (lines[-1].index("."), height - 1)

    return {
        "field": field,
        "start": start,
        "end": end,
        "width": width,
        "height": height,
    }


def print_field_with_path(
    field: dict[Coord, str], width: int, height: int, path: set[Coord]
):
    for y in range(height):
        for x in range(width):
            if (x, y) in path:
                print("O", end="")
            else:
                print(field[(x, y)], end="")
        print()


UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)


STEP_VECTORS = [UP, RIGHT, DOWN, LEFT]


def part_1():
    data = parse_input("input.txt")

    field = data["field"]
    start = data["start"]
    end = data["end"]

    def get_neighbors(coord: Coord, path: set[Coord]) -> list[Coord]:
        result = []

        for vector in STEP_VECTORS:
            possible = (coord[0] + vector[0], coord[1] + vector[1])

            if possible in path or possible not in field or field[possible] == "#":
                continue

            # print("Checking", possible, "with vector", vector, field[possible])

            if field[possible] == ".":
                result.append(possible)
            elif field[possible] == ">" and vector == RIGHT:
                result.append(possible)
            elif field[possible] == "v" and vector == DOWN:
                result.append(possible)

        return result

    def walk_until_possible(segment_start: Coord, path: set[Coord]):
        path = path.copy()

        current = segment_start
        while True:
            path.add(current)

            if current == end:
                return end, path

            neighbors = get_neighbors(current, path)

            if len(neighbors) != 1:
                return current, path

            current = neighbors[0]

    paths_till_end = []

    queue = deque([(start, {start})])
    while len(queue) > 0:
        current, path = queue.popleft()

        if current == end:
            paths_till_end.append(path)
            continue

        neighbors = get_neighbors(current, path)
        # print("Neighbors of", current, "are", neighbors)
        for neighbor in neighbors:
            segment_end, extended_path = walk_until_possible(
                neighbor, path | {neighbor}
            )
            # print("Appending", segment_end, extended_path)
            queue.append((segment_end, extended_path))

    # print_field_with_path(data["field"], data["width"], data["height"], path)

    # The start field does not count into the path length, so we need to subtract 1
    return max(len(path) - 1 for path in paths_till_end)


def part_2():
    data = parse_input("input.txt")

    field = data["field"]
    start = data["start"]
    end = data["end"]

    # replace every slope with a normal field
    for coord, value in field.items():
        if value in ">vV<^":
            field[coord] = "."

    def get_neighbors(coord: Coord) -> list[Coord]:
        result = []

        for vector in STEP_VECTORS:
            possible = (coord[0] + vector[0], coord[1] + vector[1])
            if field.get(possible) == ".":
                result.append(possible)

        return result

    junctions = [
        start,
        *(
            coord
            for coord, value in field.items()
            if value == "." and len(get_neighbors(coord)) > 2
        ),
        end,
    ]

    # print(len(junctions))

    edges = defaultdict(set)

    # BFS on the grid to find edges between junctions
    for coord in junctions:
        visited = set()
        queue = deque([(coord, 0)])
        while len(queue) > 0:
            current, distance = queue.popleft()

            visited.add(current)

            for neighbor in get_neighbors(current):
                if neighbor in junctions and neighbor != coord:
                    edges[coord].add((neighbor, distance + 1))
                elif neighbor not in visited:
                    queue.append((neighbor, distance + 1))

    def dfs(from_vertex: tuple, goal: tuple, seen: set=set()) -> list:
        """ Recursive DFS to find all path lengths from from_vertex to goal.

        Args:
            grid (_type_): _description_
            edges (dict[tuple, set]): Adjacency dictionary mapping vertex to a set of (vertex, distance)
            from_vertex (tuple): The current vertex
            goal (tuple): The final vertex we want to reach
            seen (set, optional): To track visisted vertices. First call will set it to empty.

        Returns:
            list: lengths of all valid paths
        """
        if from_vertex == goal:
            return [0] # Found a path, return a list with length 0 (since no more distance is needed)

        seen.add(from_vertex) # tp prevent backtracking in THIS path
        path_lengths = []

        # explore each connected vertex
        for next_vertex, distance in edges[from_vertex]:
            if next_vertex not in seen: # prevent backtracking for this path
                # recursively call from the next vertex onwards
                for path_len in dfs(next_vertex, goal, seen):
                    path_lengths.append(path_len + distance) # adjust each length by adding the current dist

        seen.remove(from_vertex) # to allow other paths to visit this vertex

        return path_lengths

    # use recursive function from reddit, faster than my version by 10 seconds (20 vs 30)
    return max(dfs(start, end))

    # DFS to find the longest path, Gabor version
    # path_till_end = []

    # queue = deque([(start, {start}, 0)])
    # while len(queue) > 0:
    #     current, path, length = queue.pop()

    #     if current == end:
    #         # print(length, len(path))
    #         path_till_end.append((path, length))
    #         continue

    #     neighbors = edges[current]
    #     for neighbor, distance in neighbors:
    #         if neighbor not in path:
    #             queue.append((neighbor, path | {neighbor}, length + distance))

    # return max(length for _, length in path_till_end)



if __name__ == "__main__":
    print("Part 1:", part_1())
    print("Part 2:", part_2())
