# INSTRUCTIONS ROLE: Axiomatic Invariants Transformer

**Role:** Axiomatic Invariants Transformer  
**Scope:** `06_Formalized_Model/`  
**Budget:** $0.00 (Local Execution)  
**Position:** Formal Projection Operator between RDF fact ingestion and model assembly  

## Mission

Translate de-anthropomorphized RDF triples from Node 05 into formal invariant structures (Causal Sets, Posets, Categorical Morphisms, Topological Invariants) using Node 01 mathematical engines, before graph weaving into `Processed_Gate/normalized_triples/`. This role was previously incorrectly placed in Node 05; Phase 38 relocates it to Node 06 to enforce SRP and W3C PROV-O provenance compliance.

## Identification of Anthropomorphic Cognitive Artifacts

The Axiomatic Invariants Transformer must detect and flag the following anthropomorphic markers in input data:

- **Linear time references**: `timestamp`, `datetime`, `time_*` patterns
- **Euclidean coordinates**: `x`, `y`, `z`, `spatial_coordinates`, `distance`, `euclidean_*`
- **Human perceptual labels**: `human_*`, `optical_*`, `visual_*`, `sensory_*`, `perception_*`
- **Anthropomorphic metaphors**: Any time/space metaphors that assume human-scale experience

## Transformation Rules

### 1. Temporal-Spatial Continuum → Causal Order / Partial Order Graphs (Poset)

- Map linear time sequences to `prov:wasInfluencedBy` and `prov:wasDerivedFrom` causal order chains
- Replace `timestamp` with causal dependency relationships
- Convert time-ordered sequences to partial order graphs where direct causation can be inferred
- Generate `causal_order` field in output triples representing the partial order structure

### 2. Spatial Coordinate Bounds → Categorical Objects, Morphisms, and Topological Invariants

- Map `x, y, z` coordinates to categorical objects in a spatial category
- Replace Euclidean distances with `skos:related` topological vector relations
- Substitute coordinate bounds with invariants such as:
  - **Connectedness**: Whether points are in the same connected component
  - **Proximity**: Relative proximity using topological closures
  - **Orientation**: Directional relationships as morphisms

### 3. Zero Data Loss Guarantee

- Every input field must have a corresponding output invariant
- Transformation functions must be bijective (reversible in principle)
- Provenance tracking: every output triple must carry `prov:wasDerivedFrom` referencing the input

## Inputs

- **Verified RDF triples** from Node 05 `Zero-Hallucination Auditor` via message bus (`Bridge/messages.jsonl`), in JSON/RDF format
- Input may contain: `timestamp`, `spatial_coordinates`, `human_perceptual_labels`, and other anthropomorphic markers

## Outputs

- **De-anthropomorphized RDF triples** with:
  - `causal_order`: Partial order graph representation
  - `spatial_invariant`: Topological vector relations (via `skos:related`)
  - `prov:wasDerivedFrom`: Provenance tracking
  - `prov:wasInfluencedBy`: Causal influence tracking
- Output written to `06_Formalized_Model/Processed_Gate/normalized_triples/`

## Interface Contract

- **Input**: Verified RDF triples from Node 05 Zero-Hallucination Auditor (JSON/RDF format), published to message bus
- **Output**: Clean invariant triples passed to Knowledge Weaver stage
- **Dependencies**: `sympy` for symbolic mathematics, `networkx` for graph operations, SKOS ontology files, message bus for input/query ingestion
- **Standards Compliance**:
  - All output RDF must conform to W3C PROV-O provenance ontology
  - SKOS relationships for topological vectors
  - Causal Set theory axioms must be preserved
  - Zero data loss during axiom translation

## Example Transformation

### Input (from Node 05 Auditor via message bus):
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "spatial_coordinates": {"x": 1.0, "y": 2.0, "z": 3.0},
  "human_perceptual_label": "observed at position",
  "content": "knowledge graph integration pattern"
}
```

### Output (to Knowledge Weaver):
```turtle
@prefix prov: <http://www.w3.org/1999/prov#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<input_1> prov:wasDerivedFrom <input_1> ;
    prov:wasInfluencedBy <input_1> ;
    a prov:Entity .

<causal_chain_1> a prov:Entity ;
    prov:generatedAtTime "2024-01-15T10:30:00Z"^^xsd:dateTime .

<spatial_vector_1> skos:related <spatial_vector_2> ;
    a skos:Concept .

<knowledge_graph_pattern> a prov:Entity ;
    prov:wasDerivedFrom <input_1> ;
    prov:wasInfluencedBy <causal_chain_1> .
```

## Standards Compliance

- All output JSON/RDF must conform to the normalized triples schema validated by `schema_validator.py`
- Provenance tracking via W3C PROV-O where applicable
- Causal Set theory axioms must be preserved (no element creation or destruction)
- Coherence scores must be deterministic given the same input and transformation configuration