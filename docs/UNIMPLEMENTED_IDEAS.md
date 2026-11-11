# Unimplemented Ideas & Backlog (Phase 22.1 Audit)

Audit of legacy directives and reports in `Bridge/in/` and `Bridge/out/` (including subfolders) performed during Phase 22.1 (v3.1.1). All analyzed legacy files moved to `Bridge/trash/`.

## Backlog / Unimplemented Ideas

1. **Missing Python packages** (from ENVIRONMENT_SPECS): `rdflib`, `dspy-ai`, `pysr`, `giotto-tda`, `gudhi`, `ollama` (Python client) — not installed. Blocks RDF/knowledge graph work, DSPy programming, symbolic regression, TDA, Ollama API integration.
2. **C/C++ compiler missing** (no gcc, no cl.exe) — blocks PySR, Lean, symbolic regression toolchains requiring native compilation. Install MinGW-w64 or VS Build Tools.
3. **AnythingLLM not detected** — no data directory found; RAG/local LLM integration via AnythingLLM requires installation and configuration.
4. **No NVIDIA GPU / CUDA** — LLM inference runs on CPU via Ollama; heavier models (qwen2.5-coder:14b, 9 GB) may be too large for 16 GB RAM CPU-only inference.
5. **Ollama models not loaded into VRAM** — 6 models downloaded but none currently loaded (`ollama ps` empty).
6. **Aggregator isolation enforcement** — Node 05 roles communicate exclusively via universal message bus; node-local bridge/in/out bindings removed (verify continued compliance).

## Status

All legacy directives (Phase 16–21) and their execution reports have been audited and archived to `Bridge/trash/`. No critical unimplemented architectural blockers beyond the environment/toolchain gaps listed above.
