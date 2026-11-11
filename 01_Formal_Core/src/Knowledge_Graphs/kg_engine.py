"""
Knowledge Graph Engine for Formal Core.

Handles noise-free triple insertion, validation, projection mapping,
and serialization. Uses NetworkX as the underlying graph backend with an
optional rdflib-compatible interface for RDF/Turtle interoperability.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

try:  # pragma: no cover - optional dependency
    import networkx as nx

    _HAS_NETWORKX = True
except ImportError:  # pragma: no cover
    nx = None  # type: ignore[assignment]
    _HAS_NETWORKX = False


class KnowledgeGraphEngine:
    """In-memory RDF-style knowledge graph backed by NetworkX.

    Stores noise-free triples of the form (subject, predicate, object)
    and supports querying, validation, projection mapping, and export.
    """

    def __init__(self) -> None:
        self.triples: List[Tuple[str, str, str]] = []
        self._entities: Set[str] = set()
        self._predicates: Set[str] = set()
        if _HAS_NETWORKX:
            self._graph: "nx.DiGraph" = nx.DiGraph()
        else:
            self._graph = None  # type: ignore[assignment]

    # ------------------------------------------------------------------
    # Triple management
    # ------------------------------------------------------------------

    def add_fact(self, subject: str, predicate: str, object_: str) -> None:
        """Adds a formal triple (S, P, O) to the core graph.

        Duplicate triples are ignored to keep the graph noise-free.
        """
        fact = (subject.strip(), predicate.strip(), object_.strip())
        if not all(fact):
            raise ValueError("Subject, predicate, and object must not be empty.")
        if fact not in self.triples:
            self.triples.append(fact)
            self._entities.add(fact[0])
            self._entities.add(fact[2])
            self._predicates.add(fact[1])
            if self._graph is not None:
                self._graph.add_edge(fact[0], fact[2], predicate=fact[1])

    def add_triples(self, triples: List[Tuple[str, str, str]]) -> int:
        """Bulk-insert triples. Returns the number of newly added facts."""
        before = len(self.triples)
        for subject, predicate, object_ in triples:
            self.add_fact(subject, predicate, object_)
        return len(self.triples) - before

    def remove_fact(self, subject: str, predicate: str, object_: str) -> bool:
        """Removes a triple if present. Returns True if removed."""
        fact = (subject.strip(), predicate.strip(), object_.strip())
        if fact in self.triples:
            self.triples.remove(fact)
            if self._graph is not None and self._graph.has_edge(fact[0], fact[2]):
                self._graph.remove_edge(fact[0], fact[2])
            return True
        return False


    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def query_entity(self, entity: str) -> List[Tuple[str, str, str]]:
        """Retrieves all triples associated with an entity (as subject or object)."""
        entity = entity.strip()
        return [t for t in self.triples if t[0] == entity or t[2] == entity]

    def query_by_predicate(self, predicate: str) -> List[Tuple[str, str, str]]:
        """Retrieves all triples with a given predicate."""
        predicate = predicate.strip()
        return [t for t in self.triples if t[1] == predicate]

    def get_neighbors(self, entity: str) -> List[str]:
        """Returns direct neighbors of an entity in the graph."""
        entity = entity.strip()
        neighbors: Set[str] = set()
        for subject, _, object_ in self.triples:
            if subject == entity:
                neighbors.add(object_)
            elif object_ == entity:
                neighbors.add(subject)
        return sorted(neighbors)

    def has_entity(self, entity: str) -> bool:
        """Checks whether an entity exists in the graph."""
        return entity.strip() in self._entities


    # ------------------------------------------------------------------
    # Projection & invariant helpers
    # ------------------------------------------------------------------

    def get_projections(self, entity: str) -> List[str]:
        """Returns DomainProjection objects linked to an entity via hasProjection."""
        return [
            object_
            for subject, predicate, object_ in self.triples
            if subject == entity and predicate == "core:hasProjection"
        ]

    def get_invariants(self, entity: str) -> List[str]:
        """Returns InvariantProperty objects linked to an entity via hasInvariant."""
        return [
            object_
            for subject, predicate, object_ in self.triples
            if subject == entity and predicate == "core:hasInvariant"
        ]

    def get_equivalents(self, entity: str) -> List[str]:
        """Returns entities equivalent to the given entity via isEquivalentTo."""
        return [
            object_
            for subject, predicate, object_ in self.triples
            if subject == entity and predicate == "core:isEquivalentTo"
        ]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> Dict[str, object]:
        """Validates graph integrity: duplicate-free triples, known entities/predicates.

        Returns a report dict with counts and any detected issues.
        """
        issues: List[str] = []
        seen: Set[Tuple[str, str, str]] = set()
        duplicates: List[Tuple[str, str, str]] = []

        for triple in self.triples:
            if triple in seen:
                duplicates.append(triple)
            seen.add(triple)

        if duplicates:
            issues.append(f"{len(duplicates)} duplicate triple(s) detected.")

        empty_fields = [
            t for t in self.triples if not t[0] or not t[1] or not t[2]
        ]
        if empty_fields:
            issues.append(f"{len(empty_fields)} triple(s) with empty field(s).")

        return {
            "triple_count": len(self.triples),
            "entity_count": len(self._entities),
            "predicate_count": len(self._predicates),
            "duplicates": duplicates,
            "issues": issues,
            "valid": len(issues) == 0,
        }

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def export_triples(self) -> List[Tuple[str, str, str]]:
        """Returns a copy of all stored triples."""
        return list(self.triples)

    def export_turtle(self, prefix_map: Optional[Dict[str, str]] = None) -> str:
        """Serializes the graph to Turtle format."""
        prefixes = prefix_map or {"core": "http://discovery.engine/core#"}
        lines: List[str] = []
        for pfx, iri in prefixes.items():
            lines.append(f"@{pfx}: <{iri}> .")
        lines.append("")
        for subject, predicate, object_ in self.triples:
            lines.append(
                f"{subject} {predicate} {object_} ."
            )
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, object]:
        """Exports the graph as a plain dictionary for JSON serialization."""
        return {
            "triples": [list(t) for t in self.triples],
            "entities": sorted(self._entities),
            "predicates": sorted(self._predicates),
        }

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self.triples)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(triples={len(self.triples)})"


if __name__ == "__main__":
    kg = KnowledgeGraphEngine()
    kg.add_fact("core:Energy", "core:isEquivalentTo", "core:MassScalar")
    kg.add_fact("core:Energy", "core:hasProjection", "core:PhysicsProjection")
    kg.add_fact("core:Energy", "core:hasInvariant", "core:EnergyConservation")
    report = kg.validate()
    print(f"KG Engine Initialized. Triples count: {len(kg.export_triples())}")
    print(f"Validation report: {report}")
    print(f"Neighbors of core:Energy: {kg.get_neighbors('core:Energy')}")

