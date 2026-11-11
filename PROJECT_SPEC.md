# PROJECT_SPEC — Discovery Engine (v3.7.0 / Phase 28)

## 1. Project Goal
Zero-Budget Open-Source Autonomous Discovery Engine & Knowledge Graph Formalization.

## 2. Hardware & Stack Specs
- **Python:** 3.12.7
- **Host OS:** Windows 11 Pro
- **CPU:** AMD Ryzen 5 5625U (6 cores / 12 threads)
- **RAM:** 16 GB
- **Inference:** CPU-bound Ollama (`qwen2.5-coder`, `llama3.1:8b`, `qwen2.5:7b`). No NVIDIA CUDA / Dedicated GPU.
- **Core Libraries:** NetworkX, SymPy, PyTorch (CPU-mode), Pure Python Fallback Engines.
- **Budget Limit:** $0.00 (No external paid APIs, Vector DBs, or cloud services).

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
- **ADR-0004:** 3-File Memory Protocol & Git Synchronization Standard (`PROJECT_SPEC.md` Specification + `PROJECT_CONTEXT.md` Data Plane + `PROJECT_STATE.md` Control Plane & Gateway Report; local Git state persistence after every directive).
- **ADR-0007:** Pure Python Zero-Dependency Fallback Engines.

## 6. Definition of Done (DoD)
- [ ] All Python files pass `py_compile`.
- [ ] Zero ungrounded or external dependencies.
- [ ] `PROJECT_STATE.md` updated and synchronized to v3.7.0 / Phase 28.

---

*Source: `Bridge/in/directive-phase27-v3.6.0.json` (directive:phase27, v3.6.0, system.master_architect → cline.executor)*