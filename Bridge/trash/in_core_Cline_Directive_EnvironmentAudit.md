# TASK DIRECTIVE: System & Environment Telemetry Audit

**Target Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine`
**Sender:** Gemini Notebook (System Architect)
**Executor:** Cline (VS Code System Engineer)
**Goal:** Gather precise system specifications, Python libraries, GPU/Hardware state, Ollama configuration, and environment capabilities to eliminate architectural assumptions.

---

## 1. Required Telemetry Actions (PowerShell / Terminal)

Please run PowerShell commands to inspect the local Windows environment and record verifiable facts:

### A. Python & Toolchain Telemetry
- Check Python version: `python --version`
- Check pip environment for installed packages: `pip list` (specifically filter for `sympy`, `rdflib`, `networkx`, `dspy-ai`, `torch`, `pysr`, `giotto-tda`, `gudhi`, `ollama`, `requests`).
- Check C/C++ build tools availability: `gcc --version` or `cl.exe` (needed for PySR / Lean / symbolic compilers).
- Check Git status: `git --version`

### B. Hardware & Acceleration Specs
- Check GPU availability & VRAM: `nvidia-smi` (if NVIDIA GPU exists) or PowerShell WMI query `Get-CimInstance Win32_VideoController`.
- Check System RAM & CPU count: `Get-CimInstance Win32_ComputerSystem` and `Get-CimInstance Win32_Processor`.

### C. Ollama & Local Model Engine Audit
- Check if Ollama CLI is accessible: `ollama --version`
- List all locally downloaded Ollama models: `ollama list`
- Test Ollama local API endpoint connectivity: `Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get`
- Check running Ollama models: `ollama ps`

### D. AnythingLLM & Directory Telemetry
- Check AnythingLLM data directory existence in `%APPDATA%\anythingllm` or `%USERPROFILE%\.anythingllm`.
- Verify full write/read permissions across `Discovery_Engine` subdirectories.

---

## 2. Output Specification

Create a new file: `Bridge/out/ENVIRONMENT_SPECS.md` with the following structure:

```markdown
# Environment & Hardware Telemetry Report

**Timestamp:** [DATETIME]
**Host OS:** [Windows version]

## 1. Hardware Resources
- **CPU:** [Name & Core count]
- **RAM:** [Total GB]
- **GPU / VRAM:** [Model & VRAM size or N/A]

## 2. Software Toolchain
- **Python Version:** [Version]
- **Key Installed Packages:** [List matching packages]
- **C/C++ Compiler Status:** [Available / Missing]
- **Git:** [Version]

## 3. Local AI Engine (Ollama & AnythingLLM)
- **Ollama Status:** [Running / Stopped / Not found]
- **API Endpoint:** [http://localhost:11434 status]
- **Downloaded Models:** [List of models from `ollama list`]
- **AnythingLLM Integration Path:** [Path detected or Manual setup needed]

## 4. Architect Recommendations & Gaps
- [List any missing libraries or missing dependencies]
```

---

## 3. Project State Synchronization

After generating `ENVIRONMENT_SPECS.md`:
1. Update `PROJECT_STATE.md` under a new section `## System Telemetry & Hardware` linking to `ENVIRONMENT_SPECS.md`.
2. Write execution report to `Bridge/out/execution_reports/report_env_audit_[TIMESTAMP].md`.
