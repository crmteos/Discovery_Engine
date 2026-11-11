# Master Directive — Phase 27 (v3.6.0)
**Role:** Master Architect (`system.master_architect`)  
**Target Execution Engineer:** Cline (`cline.executor`)  
**Protocol Version:** Single-Prompt Gateway Protocol (v2.9.0 / Phase 20)  
**Date:** 2026-11-11  
**Budget:** $0.00  

---

### 1. Objective & Scope
The goal of Phase 27 is to deploy the Project Specification (`PROJECT_SPEC.md`), sanitize the Master Project State (`PROJECT_STATE.md`), and integrate the Startpoint Meta-Prompt into the system's governance structure, aligning the Discovery Engine with the AI Project Calibrator standards.

---

### 2. Execution Tasks (Step-by-Step for Cline)

#### Task 1: Create `PROJECT_SPEC.md` at Project Root
Create `PROJECT_SPEC.md` with the following formal configuration:
- **Project Goal:** Zero-Budget Open-Source Autonomous Discovery Engine & Knowledge Graph Formalization.
- **Hardware & Stack Specs:**
  - Python 3.12.7, Windows 11 Pro, AMD Ryzen 5 5625U (6 cores / 12 threads), 16 GB RAM.
  - Inference: CPU-bound Ollama (`qwen2.5-coder`, `llama3.1:8b`, `qwen2.5:7b`). No NVIDIA CUDA / Dedicated GPU.
  - Core Libraries: NetworkX, SymPy, PyTorch (CPU-mode), Pure Python Fallback Engines.
  - Budget Limit: $0.00 (No external paid APIs, Vector DBs, or cloud services).
- **Prompting & Interaction Protocols:**
  - Strict Transactional Protocol: No first-person pronouns ("I", "My"), no emotional/sycophantic noise.
  - Strict Code Diff Rule: Target diffs with line numbers and file paths; no full-file rewrites.
  - Proof of Correctness: Mathematical or logical proof required before accepting code changes.
- **Token Budget Constraints:**
  - Max Session Length: 15–20 transactions before mandatory context reset.
  - Reset Triggers: Module shift, attention dispersion (RoPE limit), repetitive debugging loops.
- **Architectural Decision Records (ADRs):**
  - ADR-0001: Dual-Vertical 2-File Standard (`PROJECT_STATE.md` Control Plane + `PROJECT_CONTEXT.md` Data Plane).
  - ADR-0002: Non-destructive Trash Lifecycle Bin (`Bridge/trash/`).
  - ADR-0003: Single-Prompt Gateway Protocol.
  - ADR-0007: Pure Python Zero-Dependency Fallback Engines.
- **Definition of Done (DoD):**
  - [ ] All Python files pass `py_compile`.
  - [ ] Zero ungrounded or external dependencies.
  - [ ] `PROJECT_STATE.md` updated and synchronized to v3.6.0 / Phase 27.

#### Task 2: Sanitize & Synchronize `PROJECT_STATE.md`
- Update Header Metrics: `VERSION: v3.6.0 | PHASE: Phase 27 | SYSTEM READINESS: 🟢 100% Core Deployed`.
- Record Phase 27 milestone under Execution History.
- Ensure `PROJECT_STATE.md` remains clean and free from verbose, uncompacted log noise.

#### Task 3: Deploy Startpoint Meta-Prompt Standard
- Save `Startpoint Meta-Prompt` template into `docs/STARTPOINT_META_PROMPT.md` for standardized copy-paste usage at the start of new chat sessions.

#### Task 4: System Verification & Reporting
1. Run syntax verification: `python3 -m py_compile scripts/*.py` (or relevant scripts).
2. Validate system manifest: `python3 -c "import json; json.load(open('system_manifest.json'))"`.
3. Run E2E test pipeline: `python3 tests/e2e/test_e2e_pipeline.py`.
4. Log execution via `bus_manager.py` with payload file.
5. Save Execution Report to `Bridge/out/execution_reports/report_phase27_v3.6.0_[TIMESTAMP].md`.

---

### 3. Verification Criteria
- `test -f PROJECT_SPEC.md` → exit_code: 0
- `test -f docs/STARTPOINT_META_PROMPT.md` → exit_code: 0
- E2E Benchmark tests: 4/4 stages PASSED.

