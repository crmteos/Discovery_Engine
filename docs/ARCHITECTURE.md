# System Architecture

## Overview

The Discovery Engine framework consists of four primary modules:

1. **01_Formal_Core** — Symbolic reasoning, knowledge graphs, and formal ontologies.
2. **02_NeuroSymbolic_Bridge** — LLM grounding via DSPy, zero-hallucination validation, and local RAG.
3. **03_Multimodal_Interface** — Multimodal decoders for text, visual, and audio/video output.
4. **04_Discovery_Engine** — Automated discovery via symbolic regression and topological data analysis.

## Communication Bridge

The `Bridge/` directory serves as the asynchronous communication gateway between the Gemini Notebook (Architecture & Discovery Lead) and Cline (VS Code Infrastructure Engineer):

- `Bridge/in/` — Incoming directive files from Gemini
- `Bridge/out/` — Output execution logs and reports for Gemini