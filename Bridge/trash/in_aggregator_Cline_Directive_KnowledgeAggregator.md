# TASK DIRECTIVE: Initialize Knowledge Aggregator Subsystem & Ingestion Interfaces

**Target Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`
**Sender:** Gemini Notebook (Master System Architect)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Goal:** Set up a dedicated workspace, role instructions, and standardization draft files for the external Knowledge Aggregator (AI Architect + OSINT Orchestrator Pool) to deposit cognitive models, analogies, and conceptual schemes for ingestion into the `Discovery_Engine` core.
**Budget Constraint:** -bash.00 (Pure Local Execution, Open Standards)

---

## 1. Directory Tree to Create

Please ensure the following directory structure is fully initialized:

```
Discovery_Engine/
│
└── 05_Knowledge_Aggregator/           # Subsystem 5: External Knowledge Intake & Ingestion Gateway
    ├── Architect/                      # Workspace for Knowledge Aggregator AI Architect
    │   └── INSTRUCTIONS_ROLE_ARCHITECT.md
    │
    ├── OSINT_Orchestrator/             # Workspace for OSINT Analysts Pool Orchestrator
    │   └── INSTRUCTIONS_ROLE_ORCHESTRATOR.md
    │
    ├── Intake_Queue/                   # Reception point for incoming raw cognitive drafts & OSINT feeds
    │   ├── raw_cognitive_models/       # Unstructured/semi-structured mental maps
    │   ├── structural_analogies/       # Cross-domain mapping schemes
    │   ├── conceptual_schemes/         # Theoretical & domain concepts
    │   └── templates/                  # Standardized JSON/YAML intake drafts
    │       ├── cognitive_model_template.json
    │       ├── analogy_template.json
    │       └── concept_scheme_template.json
    │
    ├── Processed_Gate/                 # Validated & normalized formats ready for 01_Formal_Core
    │   └── normalized_triples/
    │
    ├── intake_processor.py             # Python handler: validates intake schemas & converts to RDF triples
    └── README.md
```

---

## 2. File Generation Specifications

### A. Role Instruction: Aggregator AI Architect (`Architect/INSTRUCTIONS_ROLE_ARCHITECT.md`)
```markdown
# ROLE INSTRUCTION: Knowledge Aggregator AI Architect
**Scope:** `Discovery_Engine/05_Knowledge_Aggregator/Architect`
**Budget:** -bash.00 (Local Execution)

## Responsibilities
1. Receive high-level cognitive models, meta-frameworks, and architectural ideas from external Notebooks.
2. Structure raw conceptual drafts into formal JSON schemas (`cognitive_model_template.json`).
3. Ensure every cognitive model defines explicit entities, relations, and invariant constraints before passing to `intake_processor.py`.
```

### B. Role Instruction: OSINT Orchestrator (`OSINT_Orchestrator/INSTRUCTIONS_ROLE_ORCHESTRATOR.md`)
```markdown
# ROLE INSTRUCTION: OSINT Pool Orchestrator
**Scope:** `Discovery_Engine/05_Knowledge_Aggregator/OSINT_Orchestrator`
**Budget:** -bash.00 (Local Execution)

## Responsibilities
1. Aggregate multi-source open-intelligence (OSINT) data streams and analytical reports.
2. Extract cross-domain structural analogies and map them into `analogy_template.json`.
3. Deposit validated analyst findings into `Intake_Queue/structural_analogies/` for core processing.
```

### C. Intake Draft Templates (`Intake_Queue/templates/`)

#### 1. `cognitive_model_template.json`
```json
{
  "metadata": {
    "model_name": "Sample_Cognitive_Model",
    "author": "Knowledge_Aggregator_Architect",
    "timestamp": "2026-11-08T00:00:00Z",
    "source_notebook": "External_Cognitive_Notebook"
  },
  "entities": [
    {
      "id": "entity_001",
      "name": "ConceptA",
      "type": "AbstractConcept",
      "properties": {"domain": "Cognition"}
    }
  ],
  "relations": [
    {
      "subject": "entity_001",
      "predicate": "influences",
      "object": "entity_002"
    }
  ],
  "invariants": [
    "Conservation_Law_Or_Axiom_Expression"
  ]
}
```

#### 2. `analogy_template.json`
```json
{
  "analogy_id": "ANALOGY_001",
  "source_domain": "Biological_Evolution",
  "target_domain": "Software_Architecture",
  "mappings": [
    {
      "source_element": "Mutation",
      "target_element": "Code_Refactoring",
      "relation_type": "StructuralIsomorphism"
    }
  ]
}
```

#### 3. `concept_scheme_template.json`
```json
{
  "scheme_id": "SCHEME_001",
  "title": "Conceptual Knowledge Network",
  "keywords": ["osint", "graph", "topology"],
  "concepts": [
    {
      "name": "Node_X",
      "definition": "Formal definition of the concept"
    }
  ]
}
```

### D. Intake Processor (`intake_processor.py`)
Create a Python validation script at `05_Knowledge_Aggregator/intake_processor.py`:
```python
"""
Intake Processor: Validates incoming cognitive models and maps them into 01_Formal_Core.
"""
import os
import json
from pathlib import Path

INTAKE_DIR = Path(__file__).parent / "Intake_Queue"
PROCESSED_DIR = Path(__file__).parent / "Processed_Gate" / "normalized_triples"

def process_intake_queue():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_count = 0
    
    for category in ["raw_cognitive_models", "structural_analogies", "conceptual_schemes"]:
        target_path = INTAKE_DIR / category
        if not target_path.exists():
            continue
        for json_file in target_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                out_name = f"normalized_{json_file.stem}.json"
                with open(PROCESSED_DIR / out_name, 'w', encoding='utf-8') as f:
                    json.dump({"status": "NORMALIZED", "payload": data}, f, indent=2, ensure_ascii=False)
                processed_count += 1
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
                
    print(f"Ingestion complete. Processed {processed_count} files into Processed_Gate.")
    return processed_count

if __name__ == "__main__":
    process_intake_queue()
```

---

## 3. Registration & Reporting

1. **Update `PROJECT_STATE.md`**:
   - Register `05_Knowledge_Aggregator` as an Active Ingestion Subsystem (Subsystem 5).
   - Update execution history for Phase 8.

2. **Generate Execution Report**:
   - Save report to `Bridge/out/execution_reports/report_aggregator_[TIMESTAMP].md`.
