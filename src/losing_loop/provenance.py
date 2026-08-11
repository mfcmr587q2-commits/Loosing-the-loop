from dataclasses import dataclass, field
from enum import Enum

class EdgeType(str, Enum):
    DERIVED_FROM = "derived_from"
    OBSERVED_FROM = "observed_from"
    SUPPORTED_BY = "supported_by"
    CONTRADICTED_BY = "contradicted_by"
    VALIDATED_BY = "validated_by"
    AUTHORIZED_BY = "authorized_by"
    INVALIDATED_BY = "invalidated_by"

@dataclass(frozen=True)
class Edge:
    source: str
    destination: str
    type: EdgeType

@dataclass
class ProvenanceGraph:
    nodes: set[str] = field(default_factory=set)
    edges: list[Edge] = field(default_factory=list)

    def add_node(self, node_id: str):
        self.nodes.add(node_id)

    def add_edge(self, source: str, destination: str, edge_type: EdgeType):
        self.nodes.update((source, destination))
        self.edges.append(Edge(source, destination, edge_type))

    def trace(self, node_id: str) -> list[Edge]:
        return [e for e in self.edges if e.destination == node_id or e.source == node_id]

    def verify_path(self, path: list[str]) -> bool:
        if len(path) < 2:
            return False
        for a, b in zip(path, path[1:]):
            if not any(e.source == a and e.destination == b for e in self.edges):
                return False
        return True

@dataclass
class Witness:
    source: str
    destination: str
    path: list[str]
    transferred_facts: list[str] = field(default_factory=list)

    def verify(self, graph: ProvenanceGraph) -> bool:
        return graph.verify_path(self.path) and self.path[0] == self.source and self.path[-1] == self.destination
