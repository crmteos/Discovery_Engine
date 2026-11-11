# INSTRUCTIONS ROLE: Wide Discovery Agent

**Role:** Wide Discovery Agent (Zoom Out)  
**Scope:** `05_Knowledge_Aggregator/`  
**Budget:** $0.00 (Local Execution)  

## Mission
Broad contextual query expansion and ranked link indexing. The Wide Discovery Agent takes hypotheses or queries from the Formal Core and expands them into a comprehensive candidate set using similarity analysis, coherence scoring, and contextual broadening.

## Inputs
- Queries or hypotheses from Formal Core (`01_Formal_Core/src/01_Formal_Ontologies/` or derived from `Bridge/messages.jsonl`)
- Optional: Seed query text or concept URI

## Operations
1. **Query Expansion**: Accept a raw query/hypothesis and generate expanded query variants using:
   - Term synonym/hypernym expansion via SKOS `skos:broader`/`skos:narrower` relationships
   - Related concept injection via `skos:related`
   - Phrase recombination and variant generation
2. **Candidate Retrieval**: Use `similarity_analyzer.py` (Mode A/B) to retrieve candidate links:
   - **Mode A**: Fast similarity scoring against pre-indexed candidate set
   - **Mode B**: Deep semantic similarity with vector alignment
3. **Coherence Scoring**: Score each candidate link for coherence with the original query/hypothesis
4. **Ranking**: Rank all candidates by composite coherence score and produce `link_index.json`

## Outputs
- `link_index.json` — A JSON array of ranked link candidates, each with:
  - `rank`: integer position (1-based, sorted by descending coherence score)
  - `candidate_id`: unique identifier for the candidate link/URI
  - `coherence_score`: float score (0.0–1.0), higher is more coherent
  - `source_query`: the original query/hypothesis that generated this candidate
  - `expansion_method`: "synonym", "hypernym", "related", or "phrase_variant"
  - `supporting_evidence`: optional notes on why this candidate was selected

## Interface Contract
- **Input:** Raw query string or hypothesis URI
- **Output:** `link_index.json` written to `05_Knowledge_Aggregator/roles/` or a designated output path
- **Dependencies:** `similarity_analyzer.py` (modes A/B), SKOS ontology files, `bridge/in/` message bus for input/query ingestion

## Standards Compliance
- All output JSON must conform to the `link_index.json` schema validated by `schema_validator.py`
- Provenance tracking via W3C PROV-O where applicable
- Coherence scores must be deterministic given the same input and similarity analyzer configuration

## Example Output (link_index.json)
```json
[
  {
    "rank": 1,
    "candidate_id": "http://example.org/concept/1024",
    "coherence_score": 0.94,
    "source_query": "knowledge graph integration patterns",
    "expansion_method": "hypernym",
    "supporting_evidence": "Expanded via skos:broader from 'graph' to 'knowledge graph'"
  },
  {
    "rank": 2,
    "candidate_id": "http://example.org/concept/571",
    "coherence_score": 0.88,
    "source_query": "knowledge graph integration patterns",
    "expansion_method": "related",
    "supporting_evidence": "Related concept 'schema mapping' detected in OSINT sources"
  }
]
```