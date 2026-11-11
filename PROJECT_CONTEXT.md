# Discovery Engine — PROJECT_CONTEXT.md (Master Architect Data Plane)

**Notebook Role:** Master Architect — Data Plane (Second Notebook of the Root Master Governance Pair)
**Companion File:** `PROJECT_STATE.md` — Control Plane (Master Governance, Node Registry, System Metrics)
**System Version:** v3.8.0 — Phase 29
**Date:** 2026-11-11
**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack)

---

## 1. Purpose

`PROJECT_CONTEXT.md` is the **Master Architect Data Plane** notebook. Together with `PROJECT_STATE.md` (Control Plane) it implements the **Dual-Vertical 2-File Standard** for the Master Architect (`system.master_architect`) at the project root:

| Plane | File | Responsibility |
|-------|------|----------------|
| Control Plane | `PROJECT_STATE.md` | Master governance, node registry, system metrics, execution history, versioning |
| Data Plane | `PROJECT_CONTEXT.md` | Master knowledge domain, RDF graph topology, triple normalization rules, cross-node data flow definitions |

This file is the single source of truth for all **data-plane** architectural knowledge of the Discovery Engine. Node-level data planes (e.g. `CONTEXT_DOMAIN_[NODE].md`) remain scoped to their nodes; this file governs the **global/master** data domain.

---

## 2. Master Knowledge Domain (Data Plane)

The Discovery Engine operates over a unified, mathematically grounded knowledge graph built from normalized RDF triples. The master data domain spans all nodes:

- **Node 01 — Formal Core & Discovery Engine:** RDF/OWL ontologies, knowledge graphs, symbolic AI, TDA gap detection, symbolic regression.
- **Node 05 — Knowledge Aggregator:** OSINT stream ingestion, cognitive model formation, concept normalization, triple extraction.
- **Node 06 — Formalized Target Model:** Mathematically grounded cognitive target model assembled from validated triples.
- **Node 00 — Project Interface:** Dashboard views, execution reporting, AnythingLLM gateway binding.

All data-plane artifacts flow through the **Universal Transactional JSONL Message Bus** (`Bridge/messages.jsonl`) managed by `Bridge/bus_manager.py`.

---

## 5. Cross-Node Data Flow Definitions

| Flow | Source | Destination | Transport | Schema |
|------|--------|-------------|-----------|--------|
| Directive intake | `system.master_architect` → `Bridge/in/` | `cline.executor` | Universal Message Bus (JSONL) | Directive Markdown (`.md`) |
| Concept ingestion | OSINT / raw concepts | `05_Knowledge_Aggregator/Intake_Queue/` | Node-local bridge/in | Cognitive model template JSON |
| Triple normalization | `05_Knowledge_Aggregator` | `Processed_Gate/normalized_triples/` | Internal | Normalized triple JSON |
| Graph build | Normalized triples | `01_Formal_Core/Knowledge_Graphs/kg_engine.py` | Internal import | RDF triple set |
| Target model assembly | Validated triples | `06_Formalized_Model/` | Message Bus (`model_bus_listener.py`) | ISO/IEC/IEEE 42010 3-view JSON |
| Execution reporting | `cline.executor` | `Bridge/out/execution_reports/` | File write | Markdown report |

**Isolation rule:** Node 05 roles (`aggregator.architect`, `aggregator.osint_analyst`) communicate exclusively via `Bridge/in/aggregator/` and `Bridge/out/aggregator_reports/`. They do NOT read `Bridge/in/core/` nor write `Bridge/out/execution_reports/`.

---

## 6. Master Architect Notebook Pair (v2.9.2 Standard)

The root-level Master Architect is served by exactly two notebooks:

1. **`PROJECT_STATE.md`** — Control Plane
   - Header metrics (budget, session, readiness, version, phase)
   - Execution history (Phase 16 → Phase 28)
   - Node registry & system health table
   - Communication sub-channel specification
   - Directory structure of `Bridge/`

2. **`PROJECT_CONTEXT.md`** — Data Plane (this file)
   - Master knowledge domain
   - Global RDF graph topology & invariants
   - Triple normalization rules
   - Cross-node data flow definitions

Any change to the physical data-plane structure (new schemas, new triple sources, new data-flow endpoints) MUST be recorded here first, mirroring the Control Plane rule in `PROJECT_STATE.md`.

---

## 7. Verification

- `test -f PROJECT_CONTEXT.md` → `exit_code: 0`
- `python3 -c "import json; json.load(open('system_manifest.json'))"` → `PASSED` (manifest references this file under master governance artifacts)
- `python3 test_e2e_pipeline.py` → `exit_code: 0` (4/4 stages OK)

---

## 8. Environment & Hardware Telemetry (v3.1.1)

Recorded from `Bridge/out/ENVIRONMENT_SPECS.md` (moved to `Bridge/trash/`).

| Resource | Specification |
|----------|---------------|
| Host OS | Microsoft Windows 11 Pro, Version 10.0.26300, 64-bit (ASUS-DEV) |
| CPU | AMD Ryzen 5 5625U with Radeon Graphics — 6 cores, 12 logical processors, 2300 MHz |
| RAM | ~15.4 GB (16 GB installed) |
| GPU / VRAM | AMD Radeon (TM) Graphics, 512 MB shared VRAM; No NVIDIA/CUDA |
| Python | 3.12.7 |
| Key Packages | networkx 3.7, requests 2.34.2, sympy 1.14.0, torch 2.15.0 |
| Missing Packages | rdflib, dspy-ai, pysr, giotto-tda, gudhi, ollama (Python client) |
| C/C++ Compiler | Missing (no gcc, no cl.exe) |
| Git | 2.56.0.windows.4 |
| Ollama | 0.40.14 — Running, API responding, 6 models downloaded (qwen2.5-coder:14b, gemma2:9b, llama3.1:8b, qwen2.5:7b, qwen2.5-coder-32k, qwen2.5-coder) |
| AnythingLLM | Not detected — manual setup needed |

Telemetry logic integrated into `scripts/` (`scripts/bus_status.py`). No NVIDIA GPU/CUDA; LLM inference runs on CPU via Ollama.

---

## 9. AnythingLLM Gateway REST API Topology (v3.2.0)

| Endpoint | Method | Path | Purpose |
|----------|--------|------|---------|
| Health (auth) | GET | `/auth` | Auth validation |
| Health (ping) | GET | `/ping` | Liveness ping |
| Workspaces | GET | `/workspaces` | List active workspaces |
| Chat | POST | `/workspace/{slug}/chat` | Route prompts/responses |
| Document upload | POST | `/workspace/{slug}/update-embeddings` | Sync documents |

Base URL: `http://127.0.0.1:3001/api/v1` (AnythingLLM local). Offline fallback (`offline_fallback`) when server not reachable.

---

## 10. Ollama Gateway REST API Topology (v3.8.0)

Local LLM inference is provided by the on-host Ollama server (`http://127.0.0.1:11434`), bound through `00_Project_Interface/src/ollama_gateway.py`.

| Endpoint | Method | Path | Purpose |
|----------|--------|------|---------|
| Liveness / model list | GET | `/api/tags` | Ping Ollama server; enumerate installed models |
| Inference | POST | `/api/generate` | Generate completion for a prompt on a specific model |

| Setting | Value |
|---------|-------|
| Base URL | `http://127.0.0.1:11434` |
| Model fallback chain | `qwen2.5-coder:14b` → `llama3.1:8b` → `qwen2.5:7b` |
| Offline behaviour | Graceful fallback: `--test` completes with `exit_code: 0` even when the Ollama server is unreachable |
| Budget | $0.00 (local CPU, no paid APIs) |

Telemetry from each `--test` run is posted to the Universal Message Bus (`Bridge/messages.jsonl`) via `Bridge/bus_manager.py` (`log_core_telemetry`).

---

**End of PROJECT_CONTEXT.md — Master Architect Data Plane — v3.8.0**