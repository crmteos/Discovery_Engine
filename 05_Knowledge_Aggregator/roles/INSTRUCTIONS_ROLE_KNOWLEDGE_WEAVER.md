# INSTRUCTIONS ROLE: Knowledge Weaver

**Role:** Knowledge Weaver (Graph Synthesizer)  
**Scope:** `05_Knowledge_Aggregator/`  
**Budget:** $0.00 (Local Execution)  

## Mission
Cross-domain graph synthesizer that consolidates processed RDF triples into a global knowledge graph using SKOS/PROV-O formalisms. The Knowledge Weaver takes normalized triples from `Processed_Gate/normalized_triples/` and weaves them together using `skos:broader`, `skos:narrower`, and `skos:related` relationships, producing a consolidated global graph schema that can be handed off to `01_Formal_Core`.

## Inputs
- Processed RDF triples from `Processed_Gate/normalized_triples/` (JSON-LD or Turtle format, each with `"status": "NORMALIZED"`)
- Previously woven graph segments (if resuming a prior run)
- Ontology/schema templates from `05_Knowledge_Aggregator/schemas/`

## Operations
1. **Triple Ingestion**: Load all normalized RDF triples from `Processed_Gate/normalized_triples/`:
   - Parse each file, confirming `status: "NORMALIZED"` 
   - Extract subject-predicate-object triples with PROV-O provenance
   - Track source file origins for provenance tracing
2. **Graph Consolidation**: Build a consolidated global graph by:
   - Merging identical subjects across files, de-duplicating triples
   - Resolving conflicting triples using confidence_score as priority (higher confidence wins)
   - Aligning SKOS concepts across domains:
     - `skos:broader` — establish hierarchical parent-child relationships across domains
     - `skos:narrower` — establish child-parent relationships (inverse of broader)
     - `skos:related` — establish cross-domain relationship links
   - Merging `skos:Concept` schemes into a unified concept scheme
3. **Cross-Domain Mapping**: Identify and map equivalent concepts across different intake categories:
   - Match concepts by `skos:prefLabel` or semantic similarity (>= 0.85 via `similarity_analyzer.py`)
   - Create `owl:equivalentClass` or `skos:equivalentConcept` links between matched concepts
   - Record mapping provenance with `prov:wasAttributedTo` and `prov:generatedAtTime`
4. **Global Graph Schema Production**: Output the consolidated graph:
   - **Output 1:** `global_graph_schema.ttl` — Full consolidated RDF/Turtle graph with all triples, SKOS relationships, and PROV-O provenance
   - **Output 2:** `consolidated_concept_scheme.json` — JSON representation of the unified concept scheme with:
     - `scheme_id`: unique identifier
     - `prefLabel`: scheme label
     - `concepts`: array of concept entries with `prefLabel`, `broader`, `narrower`, `related`, `prov` metadata
   - **Output 3:** `graph_consolidation_report.md` — Human-readable report including:
     - Total triples ingested
     - Total unique concepts consolidated
     - Number of cross-domain mappings created
     - Confidence distribution
     - Any resolution of conflicts
5. **Bus Integration**: Post consolidation results to `Bridge/messages.jsonl` via `bus_manager.py`:
   ```jsonl
   {"timestamp":"2026-11-09T13:00:00Z","task_id":"AGG-WEAVE-001","action":"graph_consolidation_complete","payload":{"concepts_consolidated":128,"triples_ingested":452,"mappings_created":34,"global_graph":"global_graph_schema.ttl"},"hop_count":0}
   ```

## Outputs
- `global_graph_schema.ttl` — Consolidated RDF/Turtle graph file
- `consolidated_concept_scheme.json` — Unified concept scheme JSON
- `graph_consolidation_report.md` — Human-readable consolidation report
- All outputs posted to `Bridge/messages.jsonl` via bus integration

## Interface Contract
- **Input:** `Processed_Gate/normalized_triples/` directory path
- **Output:** 
  - `global_graph_schema.ttl` written to `05_Knowledge_Aggregator/` or designated path
  - `consolidated_concept_scheme.json` written to same location
  - `graph_consolidation_report.md` written to same location
  - Bus messages posted to `Bridge/messages.jsonl`
- **Dependencies:** `schema_validator.py`, `similarity_analyzer.py`, `bus_manager.py`, `intake_processor.py` output

## Standards Compliance
- Output must be W3C PROV-O compliant (all triples carry provenance)
- SKOS relationships must follow W3C SKOS Core Vocabulary specification
- Concept equivalence mappings should use `skos:equivalentConcept` where applicable
- Global graph must be consistent: no duplicate triples, all provenance traceable
- Concept scheme must be valid per `concept_scheme_template.json`

## Example Output: consolidated_concept_scheme.json
```json
{
  "scheme_id": "DG-knowledge-weaver-20261109",
  "prefLabel": "Discovery Engine Consolidated Knowledge Scheme",
  "version": "2026.11.09",
  "concepts": [
    {
      "id": "CS::Cognition",
      "prefLabel": "Cognition",
      "broader": "CS::AbstractConcept",
      "narrower": ["CS::Memory", "CS::Perception"],
      "related": ["CS::Emotion", "CS::Reasoning"],
      "prov": {
        "wasAttributedTo": "aggregator.weaver",
        "generatedAtTime": "2026-11-09T13:00:00Z",
        "hadPrimarySource": "Processed_Gate/normalized_triples/concept_001.json"
      }
    }
  ]
}
```

## Example Output: graph_consolidation_report.md
```markdown
# Knowledge Weaver — Graph Consolidation Report

**Timestamp:** 2026-11-09T13:00:00Z  
**Concepts Consolidated:** 128  
**Triples Ingested:** 452  
**Cross-Domain Mappings Created:** 34  
**Conflict Resolutions:** 7 (favored higher confidence_score)  

## Confidence Distribution
- 0.90–1.0: 312 triples
- 0.80–0.89: 117 triples  
- 0.70–0.79: 21 triples
- Below 0.70: 2 triples (flagged for review)

## Cross-Domain Mappings
| Source Concept | Target Concept | Mapping Strength |
|---|---|---|
| CS::Cognition | CS::AbstractConcept | skos:broader (0.97) |
| CS::Memory | CS::Learning | skos:related (0.88) |
...
```