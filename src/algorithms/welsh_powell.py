from __future__ import annotations
from time import perf_counter
from typing import Dict
from src.graph.models import ConflictGraph, GraphColoringResult

COMPLEXITY = "O(V log V + E)"

def welsh_powell(graph: ConflictGraph) -> GraphColoringResult:
    start = perf_counter()
    traversal = graph.order_by_degree_desc()
    colors: Dict[str, int] = {vertex: 0 for vertex in graph.vertices()}
    current_color = 1

    for vertex in traversal:
        if colors[vertex] != 0:
            continue

        colors[vertex] = current_color

        for candidate in traversal:
            if colors[candidate] == 0 and all(colors[neighbor] != current_color for neighbor in graph.neighbors(candidate)):
                colors[candidate] = current_color

        current_color += 1

    elapsed_ms = (perf_counter() - start) * 1000
    return GraphColoringResult(
        algorithm="Welsh-Powell",
        colors=colors,
        blocks=max(colors.values(), default=0),
        order=traversal,
        elapsed_ms=elapsed_ms,
        complexity=COMPLEXITY,
    )
