from __future__ import annotations
from time import perf_counter
from typing import Dict
from src.graph.models import ConflictGraph, GraphColoringResult


COMPLEXITY = "O(m^V)"


def backtracking(graph: ConflictGraph) -> GraphColoringResult:
    start = perf_counter()
    vertices = graph.order_by_degree_desc()
    best_colors: Dict[str, int] = {}
    best_used = len(vertices)
    colors: Dict[str, int] = {vertex: 0 for vertex in vertices}

    def is_safe(vertex: str, candidate_color: int) -> bool:
        return all(colors[neighbor] != candidate_color for neighbor in graph.neighbors(vertex))

    def search(index: int, used_colors: int) -> None:
        nonlocal best_used, best_colors

        if used_colors >= best_used:
            return

        if index == len(vertices):
            best_used = used_colors
            best_colors = colors.copy()
            return

        vertex = vertices[index]
        for candidate_color in range(1, used_colors + 1):
            if is_safe(vertex, candidate_color):
                colors[vertex] = candidate_color
                search(index + 1, used_colors)
                colors[vertex] = 0

        new_color = used_colors + 1
        if new_color < best_used:
            colors[vertex] = new_color
            search(index + 1, new_color)
            colors[vertex] = 0

    search(0, 0)

    elapsed_ms = (perf_counter() - start) * 1000
    return GraphColoringResult(
        algorithm="Backtracking",
        colors=best_colors,
        blocks=max(best_colors.values(), default=0),
        order=vertices,
        elapsed_ms=elapsed_ms,
        complexity=COMPLEXITY,
        exact=True,
    )
