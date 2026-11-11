# Cline Directive: Cross-Media RDF Linking Integration

**Directive ID:** `DIR-AGG-20261109-006`  
**Target Node:** `05_Knowledge_Aggregator`  
**Role:** `aggregator.architect`  
**Budget:** `$0.00` (Local Execution Only)  

---

## 1. Objective
Extend `intake_processor.py` to perform **Cross-Media RDF Linking**. When normalizing cognitive models, analogies, or concept schemes along with associated media metadata (`image_metadata` and `video_index`), `intake_processor.py` must automatically construct semantic RDF triples binding abstract concepts to visual keys, screenshots, and video timestamp chunks via W3C `prov:hadPrimarySource` and `skos:related` predicate relationships.

---

## 2. Requirements

1. **Update `05_Knowledge_Aggregator/intake_processor.py`:**
   * Implement semantic linking logic between `cognitive_model` / `concept_scheme` entities and related `image_metadata` / `video_index` entries.
   * Generate valid RDF N-Triples / Turtle representations in `Processed_Gate/normalized_triples/`.
   * Ensure `prov:hadPrimarySource` points to media file/chunk references and `skos:related` connects media concepts to domain entities.
   * Integrate `bus_manager.py` to record transaction logs to `Bridge/messages.jsonl`.

2. **Verification & Testing:**
   * Create test intake set containing 1 cognitive model + 1 image metadata + 1 video index in `Intake_Queue/`.
   * Execute `python 05_Knowledge_Aggregator/intake_processor.py`.
   * Run `python 05_Knowledge_Aggregator/schema_validator.py` on outputs.
   * Run `python 05_Knowledge_Aggregator/bus_inspector.py` to confirm zero message bus errors.

3. **Report Generation:**
   * Save execution report to `Bridge/out/aggregator_reports/report_rdf_cross_linking_[TIMESTAMP].md`.

---

## 3. Compliance Check
- [ ] `intake_processor.py` syntax clean (`py_compile exit_code 0`)
- [ ] RDF normalized triples generated in `Processed_Gate/normalized_triples/`
- [ ] W3C PROV-O & SKOS relationships properly connected in RDF output
- [ ] `bus_inspector.py` audit passes with 0 errors
- [ ] Budget strictly maintained at $0.00
