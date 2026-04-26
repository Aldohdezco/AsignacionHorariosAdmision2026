from __future__ import annotations
from time import perf_counter
from typing import Dict, List, Set
from src.graph.models import ConflictGraph, GraphColoringResult

COMPLEXITY = "O(V^2 + E)"

def dsatur(graph: ConflictGraph) -> GraphColoringResult:
    start = perf_counter()
    colors: Dict[str, int] = {vertex: 0 for vertex in graph.vertices()}
    saturation: Dict[str, int] = {vertex: 0 for vertex in graph.vertices()}
    uncolored: Set[str] = set(graph.vertices())
    coloring_order: List[str] = []

    if not uncolored:
        return GraphColoringResult(
            algorithm="DSATUR",
            colors={},
            blocks=0,
            order=[],
            elapsed_ms=0.0,
            complexity=COMPLEXITY,
        )

    first_vertex = max(uncolored, key=lambda vertex: (graph.degree(vertex), vertex))
    colors[first_vertex] = 1
    coloring_order.append(first_vertex)
    uncolored.remove(first_vertex)

    while uncolored:
        def sort_key(vertex: str) -> tuple[int, int, str]:
            return (saturation[vertex], graph.degree(vertex), vertex)

        vertex = max(uncolored, key=sort_key)
        used_colors = {colors[neighbor] for neighbor in graph.neighbors(vertex) if colors[neighbor] != 0}

        color = 1
        while color in used_colors:
            color += 1

        colors[vertex] = color
        coloring_order.append(vertex)
        uncolored.remove(vertex)

        for neighbor in graph.neighbors(vertex):
            if colors[neighbor] == 0:
                neighbor_colors = {colors[adjacent] for adjacent in graph.neighbors(neighbor) if colors[adjacent] != 0}
                saturation[neighbor] = len(neighbor_colors)

    elapsed_ms = (perf_counter() - start) * 1000
    return GraphColoringResult(
        algorithm="DSATUR",
        colors=colors,
        blocks=max(colors.values(), default=0),
        order=coloring_order,
        elapsed_ms=elapsed_ms,
        complexity=COMPLEXITY,
    )
