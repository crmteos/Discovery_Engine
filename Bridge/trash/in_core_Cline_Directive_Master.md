# TASK DIRECTIVE: Initialize Full Infrastructure for Discovery Engine

**Target Root Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine`  
**Sender:** Gemini Notebook (Architecture & Discovery Lead)  
**Executor:** Cline (VS Code Infrastructure Engineer)  
**Goal:** Create a 4-module neuro-symbolic framework structure, initialize code stubs, configurations, and setup the asynchronous communication bridge.

---

## 1. Directory Tree to Create

Please ensure the following directory tree is fully initialized:

```
Discovery_Engine/
│
├── Bridge/                           # Communication gateway
│   ├── in/                           # Incoming directive files from Gemini
│   └── out/                          # Output execution logs and reports for Gemini
│       └── execution_reports/
│
├── 01_Formal_Core/                   # Module 1: Noise-Free Formal Mathematical Core
│   ├── Symbolic_AI/                  # Symbolic reasoners (Lean 4, SymPy, z3-solver)
│   ├── Knowledge_Graphs/             # Knowledge Graphs & Graph DB schemas (NetworkX, Neo4j, RDF)
│   ├── Formal_Ontologies/            # OWL, TTL, JSON-LD formal schemas & definitions
│   └── README.md
│
├── 02_NeuroSymbolic_Bridge/          # Module 2: Grounding & LLM Interface
│   ├── Context_Engine/               # DSPy signatures, structured prompt schemas
│   ├── Grounding_Validators/         # Axiom alignment validators (Zero-hallucination checks)
│   ├── Local_RAG_Config/             # Ollama & AnythingLLM knowledge indexing configs
│   └── README.md
│
├── 03_Multimodal_Interface/          # Module 3: Multimodal State Decoders
│   ├── Decoders_Text/                # Formal state to structured Markdown/Text synthesizers
│   ├── Decoders_Visual/              # Mathematical visualizers (Manim, Matplotlib, Graphviz)
│   ├── Decoders_Audio_Video/         # Audio/Video rendering interfaces & API connectors
│   └── README.md
│
├── 04_Discovery_Engine/              # Module 4: Automatic Discovery Engine
│   ├── Symbolic_Regression/          # Formula discovery algorithms (PySR, gplearn)
│   ├── Topological_Data_Analysis/    # TDA tools for identifying knowledge gaps (Giotto-TDA, Gudhi)
│   ├── Novelty_Detectors/            # Anomaly & unmapped entity detectors
│   └── README.md
│
├── docs/                             # System Architecture & Concept Maps
│   └── ARCHITECTURE.md
│
├── .gitignore                        # Git configuration
└── README.md                         # Root System Overview
```

---

## 2. File Generation Tasks

Please create the following initial configuration and stub files:

### A. Root `.gitignore`
Create `.gitignore` at the root with standard Python, OS, and local model overrides:
```gitignore
# Virtual environments
venv/
.venv/
__pycache__/
*.pyc

# Local LLM & RAG data
*.vectorindex
*.db
*.sqlite

# Bridge temporary logs
Bridge/out/temp_*

# IDE & System
.vscode/
.DS_Store
Thumbs.db
```

### B. Root `README.md`
Create a master `README.md` introducing the architecture:
```markdown
# Discovery Engine Framework

**Discovery Engine** is a Neuro-Symbolic AI framework designed to map multi-disciplinary knowledge into a noise-free, formal mathematical core, grounded via Large Language Models, and powered by an automated discovery loop.

## Architecture Modules
1. **01_Formal_Core**: Symbolic reasoning, Knowledge Graphs, and OWL/TTL Ontologies.
2. **02_NeuroSymbolic_Bridge**: DSPy execution, Zero-Hallucination grounding, and Ollama/AnythingLLM RAG.
3. **03_Multimodal_Interface**: Decoders translating formal states into text, 2D/3D math graphics, and audio/video.
4. **04_Discovery_Engine**: Symbolic Regression (PySR) and Topological Data Analysis (Giotto-TDA) for discovery of unmapped knowledge entities.
```

### C. Initializer Stubs for Module 1 (`01_Formal_Core`)
1. In `01_Formal_Core/Formal_Ontologies/universe_base.ttl`, create a base Turtle ontology stub:
```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix core: <http://discovery.engine/core#> .

core:Entity a owl:Class ;
    rdfs:label "Universal Entity" ;
    rdfs:comment "Abstract base invariant for all objects in the formal universe." .

core:Relation a owl:Class ;
    rdfs:label "Invariant Relation" ;
    rdfs:comment "Structural mapping between two universal entities." .
```

2. In `01_Formal_Core/Symbolic_AI/sympy_core_stub.py`:
```python
"""
SymPy Mathematical Invariant Validator Stub.
"""
import sympy as sp

def validate_invariant(expression_str: str) -> bool:
    """Verifies if an algebraic expression simplifies to a valid invariant identity."""
    try:
        expr = sp.sympify(expression_str)
        return expr != sp.S.NaN
    except Exception as e:
        print(f"Validation error: {e}")
        return False

if __name__ == "__main__":
    print("SymPy Core initialized successfully.")
```

---

## 3. Execution Confirmation & Reporting

Upon completion of folder creation and file initialization:
1. Generate an execution report named `report_[TIMESTAMP].md` in `Bridge/out/execution_reports/`.
2. Report should confirm:
   - Directories created.
   - Files initialized.
   - Status of Git repository initialization (if applicable).
