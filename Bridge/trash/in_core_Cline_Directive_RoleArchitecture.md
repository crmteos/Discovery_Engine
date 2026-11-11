# TASK DIRECTIVE: Multi-Role Architecture & Project State Setup

**Target Root Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine`
**Sender:** Gemini Notebook (Architect)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Goal:** Establish specialized sub-engineer role instructions per directory and initialize a centralized, continuous project state registry (`PROJECT_STATE.md`).

---

## 1. Create Centralized State Registry (`PROJECT_STATE.md`)

Create `PROJECT_STATE.md` in the project root:

```markdown
# Discovery Engine - Master Project State

**Last Updated:** Auto-generated during initialization
**Current Phase:** Phase 1 Complete (Formal Core Initialized)

---

## System Health & Module Status

| Module Path | Assigned Role | Status | Key Artifacts |
| :--- | :--- | :--- | :--- |
| `01_Formal_Core/Formal_Ontologies` | Ontology Engineer | 🟢 Active | `universe_base.ttl`, `universal_domain.ttl` |
| `01_Formal_Core/Knowledge_Graphs` | Knowledge Graph Engineer | 🟢 Active | `kg_engine.py` |
| `01_Formal_Core/Symbolic_AI` | Symbolic AI Engineer | 🟢 Active | `sympy_core_stub.py`, `sympy_validator.py` |
| `02_NeuroSymbolic_Bridge` | Bridge & RAG Engineer | 🟡 Pending | Base folder layout ready |
| `03_Multimodal_Interface` | Multimodal Decoder Engineer | 🟡 Pending | Base folder layout ready |
| `04_Discovery_Engine` | Discovery & TDA Engineer | 🟡 Pending | Base folder layout ready |

---

## Execution History & Milestone Logs
- **Phase 0:** Workspace root and 4-module directory tree initialized.
- **Phase 1:** Module 1 (Formal Core) files, ontologies, and validators successfully deployed.

---

## Protocol for All Sub-Engineers
1. **Before Execution:** Read `PROJECT_STATE.md` to load current global context.
2. **After Execution:** Update `PROJECT_STATE.md` with new files created, test status, and timestamp.
```

---

## 2. Create Role-Specific Instruction Files (`INSTRUCTIONS_ROLE.md`)

Create dedicated instruction files in each module folder so Cline adopts the relevant persona when operating inside that folder:

### A. `01_Formal_Core/Formal_Ontologies/INSTRUCTIONS_ROLE.md`
```markdown
# ROLE: Formal Ontology Engineer
**Scope:** `01_Formal_Core/Formal_Ontologies/`
**Responsibilities:**
- Maintain Turtle (.ttl), OWL, and JSON-LD formal schemas.
- Ensure all domain entities are noise-free and mathematically defined.
- Update `PROJECT_STATE.md` after adding or modifying ontologies.
```

### B. `01_Formal_Core/Knowledge_Graphs/INSTRUCTIONS_ROLE.md`
```markdown
# ROLE: Knowledge Graph Engineer
**Scope:** `01_Formal_Core/Knowledge_Graphs/`
**Responsibilities:**
- Develop and maintain Python graph logic (NetworkX, RDFlib, Neo4j drivers).
- Ensure deterministic entity-relation queries without LLM hallucinations.
- Update `PROJECT_STATE.md` upon modifying graph engines.
```

### C. `01_Formal_Core/Symbolic_AI/INSTRUCTIONS_ROLE.md`
```markdown
# ROLE: Symbolic AI Engineer
**Scope:** `01_Formal_Core/Symbolic_AI/`
**Responsibilities:**
- Maintain SymPy, z3-solver, and Lean 4 formal logic validators.
- Verify algebraic equivalences and logical consistency of inputs.
- Update `PROJECT_STATE.md` upon deploying new validators.
```

### D. `02_NeuroSymbolic_Bridge/INSTRUCTIONS_ROLE.md`
```markdown
# ROLE: Neuro-Symbolic Bridge & RAG Engineer
**Scope:** `02_NeuroSymbolic_Bridge/`
**Responsibilities:**
- Manage DSPy signatures, structured prompt schemas, and local RAG configs (Ollama/AnythingLLM).
- Ensure model outputs are strictly grounded against `01_Formal_Core`.
- Update `PROJECT_STATE.md` upon updating bridge logic.
```

### E. `03_Multimodal_Interface/INSTRUCTIONS_ROLE.md`
```markdown
# ROLE: Multimodal Interface Engineer
**Scope:** `03_Multimodal_Interface/`
**Responsibilities:**
- Maintain state decoders for Markdown, Manim, Matplotlib, and audio/video generation.
- Translate formal graph states into human-readable visual/text representations.
- Update `PROJECT_STATE.md` upon updating decoders.
```

### F. `04_Discovery_Engine/INSTRUCTIONS_ROLE.md`
```markdown
# ROLE: Automated Discovery & TDA Engineer
**Scope:** `04_Discovery_Engine/`
**Responsibilities:**
- Maintain PySR symbolic regression algorithms and Giotto-TDA topological data analysis modules.
- Detect structural gaps and unmapped invariants in the knowledge space.
- Update `PROJECT_STATE.md` upon discovering new relations or updating discovery algorithms.

---

## 3. Reporting Requirement

Save execution confirmation log in `Bridge/out/execution_reports/report_roles_[TIMESTAMP].md`.
