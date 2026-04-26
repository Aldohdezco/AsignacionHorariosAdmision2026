from __future__ import annotations
from time import perf_counter
from typing import Dict, List, Optional
from src.graph.models import ConflictGraph, GraphColoringResult

COMPLEXITY = "O(V + E)"

def greedy_first_fit(graph: ConflictGraph, order: Optional[List[str]] = None) -> GraphColoringResult:
    start = perf_counter()
    traversal = order or graph.vertices()
    colors: Dict[str, int] = {vertex: 0 for vertex in graph.vertices()}

    for vertex in traversal:
        used_colors = {colors[neighbor] for neighbor in graph.neighbors(vertex) if colors[neighbor] != 0}
        color = 1
        while color in used_colors:
            color += 1
        colors[vertex] = color

    elapsed_ms = (perf_counter() - start) * 1000
    return GraphColoringResult(
        algorithm="Greedy (First-Fit)",
        colors=colors,
        blocks=max(colors.values(), default=0),
        order=traversal,
        elapsed_ms=elapsed_ms,
        complexity=COMPLEXITY,
    )
