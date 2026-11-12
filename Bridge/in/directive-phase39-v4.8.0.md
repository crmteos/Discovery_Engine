# 📜 ENGINE DIRECTIVE: PHASE 39 (v4.8.0)
**System Version**: `v4.8.0`  
**Target Architecture**: Node 05 (`Knowledge Aggregator`) & Node 06 (`Formalized Model`)  
**Feature Set**: Dotprompt Templating & Strict Pydantic/Zod Schemas for Genkit Flows  
**Constraint**: $0.00 Budget | Single-Prompt Protocol | Zero-Hallucination Standard  

---

### 1. Executive Summary & Objective
Phase 38 successfully relocated the `AXIOMATIC_TRANSFORMER` to Node 06 as a **Formal Projection Operator**, restoring the clean data pipeline in Node 05. 

Phase 39 introduces **Dotprompt Templating & Strict Schema Validation** across Node 05 and Node 06 Genkit Flows. This eliminates arbitrary LLM outputs by enforcing strict Pydantic/Zod schemas on all RDF extraction and axiomatic transformation outputs, guaranteeing deterministic, type-safe data serialization.

---

### 2. Mandatory Scope of Work

#### Task 39.1: Dotprompt Files Implementation
- Create `.prompt` templates in `05_Knowledge_Aggregator/prompts/` for `intake_extraction.prompt` (W3C PROV-O/SKOS extraction).
- Create `.prompt` templates in `06_Formalized_Model/prompts/` for `axiomatic_transform.prompt` (Log basis shifts $\log_{10} \to \log_2$, DFT frequency transformations).

#### Task 39.2: Strict Pydantic Schema Validation
- Implement Pydantic models in `05_Knowledge_Aggregator/src/schemas.py` and `06_Formalized_Model/src/schemas.py`.
- Ensure all Genkit Flows validate raw LLM JSON output against these schemas prior to bus publication.

#### Task 39.3: Integration Testing & Verification
- Create `tests/integration/test_genkit_dotprompt_schemas.py`.
- Verify schema validation catches malformed LLM responses gracefully without system crash.
- Run `py_compile` audit across all updated python scripts.

#### Task 39.4: Memory Triad Update & Synchronization
- Update `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, and `PROJECT_STATE.md` to `v4.8.0 / Phase 39`.
- Run `python scripts/sync_gdrive.py` to auto-update Google Drive.
- Perform `git commit -m "feat(phase39): implement dotprompt templates & strict schemas v4.8.0"` and `git push origin main`.

---

### 3. Definition of Done (DoD)
1. Dotprompt templates and Pydantic schemas created and active in Node 05 & 06.
2. Integration test `test_genkit_dotprompt_schemas.py` passes with exit code 0.
3. Memory triad updated to `v4.8.0` and synced to Google Drive + GitHub.
