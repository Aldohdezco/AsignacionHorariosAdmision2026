from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

from src.graph.models import ConflictGraph, GraphColoringResult


@dataclass
class BenchmarkStats:
    algorithm: str
    blocks_avg: float
    blocks_min: int
    blocks_max: int
    time_avg_ms: float
    time_min_ms: float
    time_max_ms: float
    time_stddev_ms: float
    iterations: int
    complexity: str
    exact: bool = False


def run_benchmark(
    graph: ConflictGraph,
    algorithm_name: str,
    algorithm_func: Callable[..., GraphColoringResult],
    iterations: int = 10,
    greedy_order: List[str] | None = None,
) -> BenchmarkStats:
    """Ejecuta un algoritmo n veces y calcula estadísticas de tiempo y bloques."""
    results: List[GraphColoringResult] = []

    for _ in range(iterations):
        if greedy_order is not None:
            result = algorithm_func(graph, greedy_order)
        else:
            result = algorithm_func(graph)
        results.append(result)

    times = [r.elapsed_ms for r in results]
    blocks = [r.blocks for r in results]

    time_avg = sum(times) / len(times)
    time_min = min(times)
    time_max = max(times)
    blocks_avg = sum(blocks) / len(blocks)
    blocks_min = min(blocks)
    blocks_max = max(blocks)

    variance = sum((t - time_avg) ** 2 for t in times) / len(times)
    time_stddev = variance**0.5

    return BenchmarkStats(
        algorithm=algorithm_name,
        blocks_avg=blocks_avg,
        blocks_min=blocks_min,
        blocks_max=blocks_max,
        time_avg_ms=time_avg,
        time_min_ms=time_min,
        time_max_ms=time_max,
        time_stddev_ms=time_stddev,
        iterations=iterations,
        complexity=results[0].complexity,
        exact=results[0].exact,
    )
