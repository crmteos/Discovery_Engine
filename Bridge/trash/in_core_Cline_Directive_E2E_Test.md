# TASK DIRECTIVE: Full End-to-End System Integration Benchmark (E2E Test Run)

**Target Root Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine`  
**Sender:** Gemini Notebook (System Architect)  
**Executor:** Cline (VS Code Infrastructure Engineer)  
**Role Scope:** Integration Testing & Benchmark Lead  
**Budget Constraint:** $0.00 (Pure Local FOSS Engine)  

---

## 🎯 Benchmark Objective

Execute a full end-to-end integration test across all 4 deployed modules of the `Discovery_Engine`. 
This benchmark simulates a multi-perspective domain problem (referencing the "Elephant & Blind Observers" paradigm), converts disjoint observations into formal triples, validates them against noise-free axioms, decodes them into multimodal representations, and automatically detects missing topological entities.

---

## 🛠️ Step-by-Step Test Pipeline (`test_e2e_pipeline.py`)

Create and execute an automated integration runner script at `test_e2e_pipeline.py` in the root of `Discovery_Engine`.

### Pipeline Execution Order:

1. **Step 1: Module 1 (Formal Core — Ingestion & Invariants)**
   - Import `KnowledgeGraphEngine` from `01_Formal_Core.Knowledge_Graphs.kg_engine`.
   - Ingest 5 synthetic nodes: `Observer_Tail`, `Observer_Trunk`, `Observer_Leg`, `Observer_Ear`, and `Elephant_System`.
   - Add relations: 
     - `Observer_Tail` -> `perceives` -> `Rope_Like_Entity`
     - `Observer_Trunk` -> `perceives` -> `Snake_Like_Entity`
     - `Observer_Leg` -> `perceives` -> `Tree_Like_Entity`
     - `Observer_Ear` -> `perceives` -> `Fan_Like_Entity`
   - Import `SymPyValidator` from `01_Formal_Core.Symbolic_AI.sympy_validator` and verify invariant equivalence: `E_total = E_tail + E_trunk + E_leg + E_ear`.

2. **Step 2: Module 2 (Neuro-Symbolic Bridge — Grounding & Axioms)**
   - Import `AxiomChecker` from `02_NeuroSymbolic_Bridge.Grounding_Validators.axiom_checker`.
   - Validate ingested facts against ontology rules in `01_Formal_Core/Formal_Ontologies/universe_base.ttl`.
   - Verify that all claims are zero-hallucination grounded in the formal core.

3. **Step 3: Module 3 (Multimodal Interface — Text & Graphics Decoding)**
   - Import `MarkdownDecoder` from `03_Multimodal_Interface.Decoders_Text.markdown_decoder`.
   - Render the complete state of the Knowledge Graph into a structured Markdown summary.
   - Import `MathVisualizer` from `03_Multimodal_Interface.Decoders_Visual.math_visualizer`.
   - Export Graphviz DOT schema representation of the unified state graph.

4. **Step 4: Module 4 (Discovery Engine — Topology & Gap Detection)**
   - Import `TDAGapFinder` from `04_Discovery_Engine.Topological_Data_Analysis.tda_gap_finder`.
   - Compute graph connectivity and identify topological gaps / unclosed loop anomalies (e.g. missing central `Universal_Elephant_Core` mapping).
   - Import `SymbolicRegressionStub` from `04_Discovery_Engine.Symbolic_Regression.symbolic_regression_stub`.
   - Run invariant formula fitting on test data vectors.
   - Import `NoveltyDetector` from `04_Discovery_Engine.Novelty_Detectors.novelty_detector`.
   - Synthesize a candidate hypothesis for the unmapped core entity (`HYPOTHESIS_UNIFIED_CORE_001`).

---

## 📊 Output Requirements

1. Execute `python test_e2e_pipeline.py`.
2. Ensure all 4 steps complete with `exit_code: 0`.
3. Save the full execution log and benchmark metrics report to:
   `Bridge/out/execution_reports/report_e2e_benchmark_[TIMESTAMP].md`.
4. Update `PROJECT_STATE.md` under `Execution History` recording the E2E test completion.

---

## 🔒 Verification & Compliance
- **Budget:** $0.00
- **Execution Mode:** Local CPU (Ollama REST + SymPy + NetworkX)
- **Code Standard:** Production-Grade Error Handling
