from collections import defaultdict
from typing import Dict


def main():
    solution_part_a: int = solve_part_a()
    print(f"Solution part A is: {solution_part_a}")

    solution_part_b: int = solve_part_b()
    print(f"Solution part B is: {solution_part_b}")


def solve_part_a() -> int:
    graph = get_graph()
    paths = bfs(graph, "COM")
    steps = 0
    for node in graph:
        path = get_path(paths, "COM", node)
        steps += len(path)
    return steps


def solve_part_b() -> int:
    graph = get_graph()
    paths = bfs(graph, "YOU")
    path = get_path(paths, "YOU", "SAN")
    return len(path) - 2


def get_graph() -> defaultdict:
    graph = defaultdict(list)
    with open("input.txt") as f:
        for line in f:
            source, dest = line.strip().split(")")
            graph[source].append(dest)
            graph[dest].append(source)
    return graph


def bfs(graph, start) -> Dict[str, str]:
    frontier = [start]
    came_from = {start: None}

    while frontier:
        current = frontier.pop()
        for node in graph[current]:
            if node in came_from:
                continue
            frontier.append(node)
            came_from[node] = current
    return came_from


def get_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    return path


if __name__ == "__main__":
    main()
