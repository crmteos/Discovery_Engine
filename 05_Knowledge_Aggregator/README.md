# 05_Knowledge_Aggregator — External Knowledge Intake & Ingestion Gateway

Subsystem 5 of the `Discovery_Engine`. Reception point for incoming raw cognitive
drafts and OSINT feeds from the external Knowledge Aggregator (AI Architect +
OSINT Orchestrator Pool). Validated drafts are normalized into RDF-style triples
and exposed via `Processed_Gate/normalized_triples/` for ingestion into
`01_Formal_Core`.

## Directory Tree

```
05_Knowledge_Aggregator/
├── Architect/
│   └── INSTRUCTIONS_ROLE_ARCHITECT.md
├── OSINT_Orchestrator/
│   └── INSTRUCTIONS_ROLE_ORCHESTRATOR.md
├── Intake_Queue/
│   ├── raw_cognitive_models/       # Unstructured/semi-structured mental maps
│   ├── structural_analogies/       # Cross-domain mapping schemes
│   ├── conceptual_schemes/         # Theoretical & domain concepts
│   └── templates/                  # Standardized JSON/YAML intake drafts
│       ├── cognitive_model_template.json
│       ├── analogy_template.json
│       └── concept_scheme_template.json
├── Processed_Gate/
│   └── normalized_triples/         # Validated & normalized formats for 01_Formal_Core
├── intake_processor.py             # Python handler: validates intake schemas & converts to RDF triples
└── README.md
```

## Usage

```bash
python 05_Knowledge_Aggregator/intake_processor.py
```

The processor scans `Intake_Queue/{raw_cognitive_models,structural_analogies,conceptual_schemes}`,
validates each JSON draft against its schema contract, and writes a normalized
envelope (`{"status": "NORMALIZED", ...}`) into
`Processed_Gate/normalized_triples/`.

## Budget

BUDGET: $0.00 | Pure local execution, open standards.
