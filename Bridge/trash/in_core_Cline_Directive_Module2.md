# TASK DIRECTIVE: Deploy Module 2 - Neuro-Symbolic Bridge & Grounding Layer

**Target Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\02_NeuroSymbolic_Bridge`
**Assigned Role:** Bridge & RAG Engineer (per `02_NeuroSymbolic_Bridge/INSTRUCTIONS_ROLE.md`)
**Global Context File:** `PROJECT_STATE.md`
**Sender:** Gemini Notebook (Architecture Lead)
**Executor:** Cline (VS Code Infrastructure Engineer)

---

## 1. Objective
Deploy the core components of **Module 2 (Neuro-Symbolic Bridge)** to connect local LLMs (Ollama / AnythingLLM) with the **01_Formal_Core**, ensuring zero-hallucination grounding and converting natural language inputs into formal ontology triples.

---

## 2. File Implementation Tasks

Please create/update the following files inside `02_NeuroSymbolic_Bridge/`:

### A. Context Engine (`02_NeuroSymbolic_Bridge/Context_Engine/dspy_signatures.py`)
Implement DSPy signature definitions for translating raw user queries into formal ontology predicates without anthropomorphic noise:

```python
"""
DSPy Signatures for Formal Core Translation.
"""
try:
    import dspy
except ImportError:
    dspy = None

class NaturalLanguageToFormalTriple:
    """
    Translates natural language statements into strict (Subject, Predicate, Object) ontology triples.
    """
    input_text = "Raw user observation or hypothesis"
    formal_triples = "Extracted RDF triples adhering strictly to universal_domain.ttl"
    confidence_score = "Mathematical confidence measure (0.0 to 1.0)"

class QueryToFormalInvariant:
    """
    Translates domain queries into symbolic math equations for SymPy verification.
    """
    user_query = "Domain query"
    symbolic_expression = "SymPy algebraic expression"

if __name__ == "__main__":
    print("DSPy Signatures initialized.")
```

### B. Grounding Validator (`02_NeuroSymbolic_Bridge/Grounding_Validators/axiom_checker.py`)
Implement an automated zero-hallucination validator that checks LLM outputs against RDF ontologies and SymPy invariants:

```python
"""
Zero-Hallucination Axiom Checker.
Validates LLM-generated triples against Formal Core Ontologies.
"""
import sys
from pathlib import Path

# Add Formal_Core to import path
formal_core_path = Path(__file__).resolve().parents[2] / "01_Formal_Core"
sys.path.append(str(formal_core_path))

from Knowledge_Graphs.kg_engine import KnowledgeGraphEngine
from Symbolic_AI.sympy_validator import InvariantValidator

class AxiomChecker:
    def __init__(self, ontology_file: str = None):
        self.kg = KnowledgeGraphEngine()
        self.validator = InvariantValidator()
        if ontology_file and Path(ontology_file).exists():
            self.kg.load_ttl(ontology_file)

    def validate_triple(self, s: str, p: str, o: str) -> dict:
        """Checks if a triple exists or is logically consistent with the Formal Core."""
        # Check direct presence or ontology consistency
        query = f"ASK {{ <http://discovery.engine/core#{s}> <http://discovery.engine/core#{p}> <http://discovery.engine/core#{o}> }}"
        exists = self.kg.query(query)
        return {
            "triple": (s, p, o),
            "is_grounded": bool(exists),
            "status": "VALIDATED" if exists else "UNGROUNDED_HYPOTHESIS"
        }

if __name__ == "__main__":
    checker = AxiomChecker()
    print("Axiom Checker initialized successfully.")
```

### C. Local RAG Config (`02_NeuroSymbolic_Bridge/Local_RAG_Config/anythingllm_bridge.json`)
Provide local RAG mapping configuration for AnythingLLM / Ollama:

```json
{
  "system_name": "Discovery_Engine_Local_RAG",
  "knowledge_base_path": "../../01_Formal_Core/",
  "indexing_rules": {
    "include_extensions": [".ttl", ".py", ".md", ".json"],
    "strip_anthropomorphic_noise": true,
    "force_formal_triples": true
  },
  "ollama_config": {
    "preferred_models": ["llama3", "qwen2.5", "deepseek-r1"],
    "temperature": 0.1,
    "top_p": 0.9
  }
}
```

---

## 3. Protocol & Reporting

1. **Pre-Execution:** Read `PROJECT_STATE.md` at project root.
2. **Post-Execution:** 
   - Update `PROJECT_STATE.md`: Change `02_NeuroSymbolic_Bridge` status from `🟡 Pending` to `🟢 Active`.
   - Update Phase log: Record completion of Phase 3 (Neuro-Symbolic Bridge Deployment).
3. **Execution Report:** Generate `Bridge/out/execution_reports/report_module2_[TIMESTAMP].md` detailing created files, syntax checks, and `PROJECT_STATE.md` updates.
