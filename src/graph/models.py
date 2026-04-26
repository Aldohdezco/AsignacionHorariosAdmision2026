from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Set

@dataclass(frozen=True)
class ClassRecord:
    id: str
    materia: str
    grupo: str
    docente: str

@dataclass
class GraphColoringResult:
    algorithm: str
    colors: Dict[str, int]
    blocks: int
    order: List[str]
    elapsed_ms: float
    complexity: str
    exact: bool = False

class ConflictGraph:
    def __init__(self) -> None:
        self.adjacency: Dict[str, Set[str]] = {}
        self.records: Dict[str, ClassRecord] = {}

    def add_vertex(self, record: ClassRecord) -> None:
        self.records[record.id] = record
        self.adjacency.setdefault(record.id, set())

    def add_edge(self, left: str, right: str) -> None:
        if left == right:
            return
        self.adjacency.setdefault(left, set()).add(right)
        self.adjacency.setdefault(right, set()).add(left)

    def neighbors(self, vertex: str) -> Set[str]:
        return self.adjacency.get(vertex, set())

    def vertices(self) -> List[str]:
        return list(self.records.keys())

    def degree(self, vertex: str) -> int:
        return len(self.neighbors(vertex))

    def order_by_degree_desc(self) -> List[str]:
        return sorted(self.vertices(), key=lambda vertex: (-self.degree(vertex), vertex))

    @classmethod
    def from_records(cls, records: List[ClassRecord]) -> "ConflictGraph":
        graph = cls()
        for record in records:
            graph.add_vertex(record)

        for index, left in enumerate(records):
            for right in records[index + 1 :]:
                if left.grupo == right.grupo or left.docente == right.docente:
                    graph.add_edge(left.id, right.id)

        return graph
