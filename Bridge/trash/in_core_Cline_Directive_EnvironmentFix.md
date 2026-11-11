# TASK DIRECTIVE: Zero-Budget Environment Optimization & Toolchain Resolution

**Target Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine`
**Sender:** Gemini Notebook (System Architect)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Goal:** Resolve hardware/software gaps identified in `ENVIRONMENT_SPECS.md` under strict $0.00 budget constraints, optimize Ollama CPU inference parameters, and install missing dependencies.

---

## 1. Context & Architectural Decisions

Based on the telemetry in `ENVIRONMENT_SPECS.md`:
* **CPU Inference Strategy:** System runs on AMD Ryzen 5 5625U (16 GB RAM, no NVIDIA CUDA GPU). To prevent RAM swapping, set **`qwen2.5:7b`** or **`qwen2.5-coder:latest`** (4.7 GB) as the default engine instead of the 14b variant.
* **$0.00 Toolchain Resolution:**
  1. Python packages (`rdflib`, `dspy-ai`, `ollama`) will be installed directly via `pip`.
  2. For C/C++ build tools (required by PySR/Lean), install **MinGW-w64** or **VS Build Tools** via Windows `winget` (free/open-source).
  3. For RAG, our Python `axiom_checker.py` + Ollama REST API acts as an autonomous backend, removing hard dependency on AnythingLLM GUI.

---

## 2. Actionable Tasks for Cline

### Task A: Update `PROJECT_STATE.md` with Telemetry Data
Add a dedicated section `## System Hardware & Environment Specs` to `PROJECT_STATE.md`:
```markdown
## System Hardware & Environment Specs
- **CPU:** AMD Ryzen 5 5625U (6 Cores / 12 Threads)
- **RAM:** 16 GB DDR4 (CPU-bound inference mode)
- **Acceleration:** AMD Radeon Integrated (No CUDA)
- **Primary Ollama Model:** qwen2.5:7b (4.7 GB) / qwen2.5-coder:latest
- **Toolchain Status:** Python 3.12.7, Git 2.56, SymPy 1.14, NetworkX 3.7
```

### Task B: Install Python Dependencies (Zero-Budget Script)
Run the following PowerShell command in the workspace terminal:
```powershell
python -m pip install --upgrade rdflib dspy-ai ollama numpy scipy matplotlib networkx sympy
```

### Task C: C/C++ Compiler Installation Guide & Verification
To enable native compilation for Module 4 tools (PySR, TDA), run one of the following free package installation commands:
```powershell
# Option 1 (MinGW w64devkit - Lightweight):
winget install w64devkit

# OR Option 2 (Visual Studio Build Tools 2022):
winget install Microsoft.VisualStudio.2022.BuildTools --override "--passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```
After installation, verify `gcc --version` or `cl.exe` in PowerShell and log the status.

### Task D: Update `Local_RAG_Config/anythingllm_bridge.json`
Update default model configuration to optimize for 16 GB CPU inference:
```json
{
  "ollama_endpoint": "http://localhost:11434",
  "default_model": "qwen2.5:7b",
  "coder_model": "qwen2.5-coder:latest",
  "max_context_length": 8192,
  "cpu_threads": 8,
  "temperature": 0.2,
  "knowledge_base_path": "01_Formal_Core/Knowledge_Graphs"
}
```

---

## 3. Reporting & Verification

1. Verify Python imports for `rdflib`, `dspy`, `ollama`.
2. Generate an execution report saved to `Bridge/out/execution_reports/report_env_fix_[TIMESTAMP].md`.
3. Update `PROJECT_STATE.md` execution log.
