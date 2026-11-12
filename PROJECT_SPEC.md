# PROJECT_SPEC — Discovery Engine (v5.3.0 / Phase 44)
**Canonical Mirror URL**: https://github.com/crmteos/Discovery_Engine/blob/main/PROJECT_SPEC.md

## 1. Project Goal
Zero-Budget Open-Source Autonomous Discovery Engine & Knowledge Graph Formalization.

## 2. Hardware & Stack Specs
- **Python:** 3.12.7
- **Host OS:** Windows 11 Pro
- **CPU:** AMD Ryzen 5 5625U (6 cores / 12 threads)
- **RAM:** 16 GB
- **Inference:** Dual-Provider Inference Engine:
  - Local Ollama REST (`http://127.0.0.1:11434`), model fallback chain `qwen2.5-coder:14b` → `llama3.1:8b` → `qwen2.5:7b`, implemented in `00_Project_Interface/src/ollama_gateway.py` with liveness ping (`/api/tags`) and graceful offline fallback.
  - Google AI Studio API via `google-genai` SDK, model chain `gemini-2.5-flash` → `gemini-2.0-flash` → `gemini-1.5-flash`, implemented in `00_Project_Interface/src/google_ai_gateway.py` with API key resolution and fallback chain.
- **Gateway:** Local Ollama REST (`http://127.0.0.1:11434`), model fallback chain `qwen2.5-coder:14b` → `llama3.1:8b` → `qwen2.5:7b`, implemented in `00_Project_Interface/src/ollama_gateway.py` with liveness ping (`/api/tags`) and graceful offline fallback.
- **Node 05 — Knowledge Aggregator:** Ollama RDF Triple Extraction — LLM extraction pipeline (`qwen2.5-coder:14b` → `llama3.1:8b` → `qwen2.5:7b`) converting unstructured text into W3C PROV-O / SKOS compliant RDF triplets with SHACL shape validation. `--llm-extract` mode in `05_Knowledge_Aggregator/src/intake_processor.py`. Offline fallback: gracefully skip LLM stage when Ollama server unreachable.
- **Core Libraries:** NetworkX, SymPy, PyTorch (CPU-mode), Pure Python Fallback Engines.
- **Budget Limit:** $0.00 (No external paid APIs, Vector DBs, or cloud services).
- **Remote Repository**: https://github.com/crmteos/Discovery_Engine.git

## 3. Prompting & Interaction Protocols
- **Strict Transactional Protocol:** No first-person pronouns ("I", "My"), no emotional/sycophantic noise.
- **Strict Code Diff Rule:** Target diffs with line numbers and file paths; no full-file rewrites.
- **Proof of Correctness:** Mathematical or logical proof required before accepting code changes.

## 4. Token Budget Constraints
- **Max Session Length:** 15–20 transactions before mandatory context reset.
- **Reset Triggers:** Module shift, attention dispersion (RoPE limit), repetitive debugging loops.

## 5. Architectural Decision Records (ADRs)
- **ADR-0001:** Dual-Vertical 2-File Standard (`PROJECT_STATE.md` Control Plane + `PROJECT_CONTEXT.md` Data Plane).
- **ADR-0002:** Non-destructive Trash Lifecycle Bin (`Bridge/trash/`).
- **ADR-0003:** Single-Prompt Gateway Protocol.
- **ADR-0004:** 3-File Memory Protocol & Git Synchronization Standard (`PROJECT_SPEC.md` Specification + `PROJECT_CONTEXT.md` Data Plane + `PROJECT_STATE.md` Control Plane & Gateway Report; primary remote endpoints: `https://github.com/crmteos/Discovery_Engine.git`; local Git state persistence after every directive).
- **ADR-0005:** Private Repository & Drive Sync Gateway Protocol. All code stored in private GitHub repo `https://github.com/crmteos/Discovery_Engine.git`. Google Drive sync limited to `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md` only (raw code/vendor files excluded). `scripts/sync_gdrive.py` automates sync. Header synchronized to `v5.0.0 / Phase 41`.
- **ADR-0008:** Enterprise Switcher & Data Residency (v5.3.0 / Phase 44). transparent switching between Google AI Studio and Vertex AI with EU/US data residency support (`europe-west1` / `us-central1`). Controlled via `--enterprise` CLI flag and `VERTEX_AI_ENABLED` / `GCP_PROJECT_ID` / `VERTEX_LOCATION` environment variables.
- **ADR-0007:** Pure Python Zero-Dependency Fallback Engines.

## 6. Definition of Done (DoD)
- [ ] All Python files pass `py_compile`.
- [ ] Zero ungrounded or external dependencies.
- [ ] `PROJECT_STATE.md` updated and synchronized to `v5.0.0 / Phase 41`.

- [ ] Run `scripts/jules_code_health.py --check` and verify JSON report.
---

*Source: `Bridge/in/directive-phase27-v3.6.0.json` (directive:phase27, v3.6.0, system.master_architect → cline.executor)*