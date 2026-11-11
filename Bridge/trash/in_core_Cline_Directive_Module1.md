# TASK DIRECTIVE: Module 1 Implementation — Formal Core & Knowledge Graph

**Target Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine`
**Sender:** Gemini Notebook (Architecture & Discovery Lead)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Goal:** Implement the formal ontology schemas, Knowledge Graph engine (RDFlib / NetworkX), and symbolic invariant validator in `01_Formal_Core`.

---

## 1. Scope of Deliverables

You will populate `01_Formal_Core` with functional code and formal specs across three sub-folders:

1. `01_Formal_Core/Formal_Ontologies/universal_domain.ttl` — Extended Turtle ontology for universal entity mapping.
2. `01_Formal_Core/Knowledge_Graphs/kg_engine.py` — Graph engine for creating, querying, and serializing noise-free knowledge triples.
3. `01_Formal_Core/Symbolic_AI/sympy_validator.py` — Symbolic validation engine to check mathematical equivalence and structural invariants.

---

## 2. File Specifications

### A. `01_Formal_Core/Formal_Ontologies/universal_domain.ttl`
Create an extended OWL/RDF ontology defining core abstract types:
```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix core: <http://discovery.engine/core#> .

# Core Classes
core:Entity a owl:Class ;
    rdfs:label "Universal Entity" ;
    rdfs:comment "Abstract invariant object representing a concept, physical entity, or state." .

core:InvariantProperty a owl:Class ;
    rdfs:label "Invariant Property" ;
    rdfs:comment "A mathematical or structural attribute invariant under coordinate transform." .

core:DomainProjection a owl:Class ;
    rdfs:label "Domain Projection" ;
    rdfs:comment "A discipline-specific language view of a universal entity (e.g. Physics vs Economics description)." .

# Relations
core:hasProjection a owl:ObjectProperty ;
    rdfs:domain core:Entity ;
    rdfs:range core:DomainProjection .

core:hasInvariant a owl:ObjectProperty ;
    rdfs:domain core:Entity ;
    rdfs:range core:InvariantProperty .

core:isEquivalentTo a owl:SymmetricProperty ;
    rdfs:domain core:Entity ;
    rdfs:range core:Entity .
```

### B. `01_Formal_Core/Knowledge_Graphs/kg_engine.py`
Create a Python script using standard libraries or `rdflib`/`networkx` stubs to manage formal triples:
```python
"""
Knowledge Graph Engine for Formal Core.
Handles noise-free triple insertion, validation, and projection mapping.
"""
from typing import Dict, List, Tuple

class KnowledgeGraphEngine:
    def __init__(self):
        self.triples: List[Tuple[str, str, str]] = []

    def add_fact(self, subject: str, predicate: str, object_: str) -> None:
        """Adds a formal triple (S, P, O) to the core graph."""
        fact = (subject.strip(), predicate.strip(), object_.strip())
        if fact not in self.triples:
            self.triples.append(fact)

    def query_entity(self, entity: str) -> List[Tuple[str, str, str]]:
        """Retrieves all triples associated with an entity."""
        return [t for t in self.triples if t[0] == entity or t[2] == entity]

    def export_triples(self) -> List[Tuple[str, str, str]]:
        return self.triples

if __name__ == "__main__":
    kg = KnowledgeGraphEngine()
    kg.add_fact("core:Energy", "core:isEquivalentTo", "core:MassScalar")
    print(f"KG Engine Initialized. Triples count: {len(kg.export_triples())}")
```

### C. `01_Formal_Core/Symbolic_AI/sympy_validator.py`
Create an expanded symbolic verification module:
```python
"""
SymPy Symbolic Invariant Validator.
Validates mathematical equations and identifies equivalent invariants.
"""
import sympy as sp

class InvariantValidator:
    @staticmethod
    def check_equivalence(expr1_str: str, expr2_str: str) -> bool:
        """Checks if two mathematical expressions are symbolically identical."""
        try:
            e1 = sp.sympify(expr1_str)
            e2 = sp.sympify(expr2_str)
            return sp.simplify(e1 - e2) == 0
        except Exception as err:
            print(f"Validation Error: {err}")
            return False

if __name__ == "__main__":
    validator = InvariantValidator()
    # Test identity E = mc^2 -> E - m*c^2 = 0
    is_valid = validator.check_equivalence("E", "m * c**2")
    print("SymPy Validator operational.")
```

---

## 3. Reporting Requirement

After completing folder updates and script generation:
1. Save the execution log in `Bridge/out/execution_reports/report_module1_[TIMESTAMP].md`.
2. Confirm syntax validation of Python files and Turtle syntax integrity.
