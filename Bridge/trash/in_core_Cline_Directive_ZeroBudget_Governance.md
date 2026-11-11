# TASK DIRECTIVE: Update Project Governance, Zero-Budget Constraint & Stateless Execution Protocol

**Target Root Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine`
**Sender:** Gemini Notebook (System Architect & Research Lead)
**Executor:** Cline (VS Code Autonomous Execution Engineer)
**Goal:** Formally integrate strict engineering constraints into `PROJECT_STATE.md` and all 6 subsystem `INSTRUCTIONS_ROLE.md` files: (1) Zero-Budget Constraint ($0.00), (2) Stateless Session Protocol, (3) Real Production-Grade Code Standard (No Toy Code), and (4) System Architect Governance.

---

## 1. Core Engineering Constraints to Institutionalize

### A. Zero-Budget Constraint (`BUDGET = $0.00`)
* **Rule:** Absolute monetary budget limit is **$0.00**.
* **Stack Requirement:** Rely 100% on free, open-source software (FOSS), local runtimes (Ollama, AnythingLLM), open-source Python libraries (SymPy, NetworkX, PySR, Giotto-TDA, rdflib, DSPy), and local hardware.
* **Prohibition:** Zero paid API keys, zero paid cloud endpoints, zero commercial SaaS dependencies. Every script and configuration must run fully offline/locally at zero cost.

### B. Stateless Autonomous Session Protocol
* **Rule:** Cline operates in clean, stateless, autonomous sessions per directive.
* **Protocol:**
  1. Every session MUST begin by reading `PROJECT_STATE.md` and the relevant local `INSTRUCTIONS_ROLE.md`.
  2. Every session MUST verify local environment conditions before execution.
  3. Every session MUST update `PROJECT_STATE.md` with execution status, timestamp, and updated system health before exit.
  4. Header requirement for all generated logs/reports: `BUDGET: $0.00 | SESSION: Autonomous Clean State`.

### C. Real Production Engineering Standard (No Toy Code)
* **Rule:** No dummy mocks, no "toy" pseudocode, no placeholder stubs masquerading as solutions.
* **Quality Standards:** All code must be production-ready Python/C++/RDF, fully syntax-checked (`python -m py_compile`), strongly typed where appropriate, defensively error-handled, and grounded in real mathematical and open-source library specifications.

### D. System Architect Governance Structure
* **System Architect (Gemini Notebook):** Strategic architecture, formal mathematical ontologies, SOTA research, directive generation, and invariant verification.
* **Execution Engineer (Cline):** Autonomous local code execution, folder/file management, environment auditing, syntax validation, git operations, and state logging.
* **System Operator / Gateway (Human User):** Human-in-the-Loop decision approval, physical file relay via `Bridge/in` and `Bridge/out`.

---

## 2. Execution Actions Required from Cline

1. **Update Root `PROJECT_STATE.md`:**
   - Add a top-level **System Constraints & Governance** section at the top of the file containing:
     - `BUDGET_LIMIT: $0.00 (Pure Open-Source & Local Hardware Stack)`
     - `EXECUTION_MODE: Stateless Autonomous Sessions`
     - `ENGINEERING_STANDARD: Production-Grade (Zero Mocks / Real Math & Code)`
     - `ROLES: System Architect (Gemini), Execution Engineer (Cline), Gateway Operator (User)`
   - Add `BUDGET: $0.00` to the header metrics of the dashboard.

2. **Update all 6 Subsystem `INSTRUCTIONS_ROLE.md` Files:**
   Modify each `INSTRUCTIONS_ROLE.md` in:
   - `01_Formal_Core/Formal_Ontologies/`
   - `01_Formal_Core/Knowledge_Graphs/`
   - `01_Formal_Core/Symbolic_AI/`
   - `02_NeuroSymbolic_Bridge/`
   - `03_Multimodal_Interface/`
   - `04_Discovery_Engine/`
   
   Insert the following mandatory header block into each role instruction file:
   ```markdown
   ---
   ROLE_BUDGET_CONSTRAINT: $0.00 (Strictly Free / Open-Source Local Stack)
   SESSION_EXECUTION_PROTOCOL: Stateless Autonomous Session
   CODE_QUALITY_BAR: Production-Grade / Non-Toy / Fully Validated
   ---
   ```

3. **Generate Execution Report:**
   - Save report to `Bridge/out/execution_reports/report_governance_[TIMESTAMP].md`.
   - Confirm updating `PROJECT_STATE.md` and all 6 `INSTRUCTIONS_ROLE.md` files.

---

## 3. Verification Criteria
- [ ] `PROJECT_STATE.md` contains the explicit Zero-Budget ($0.00) and Stateless Session governance sections.
- [ ] All 6 `INSTRUCTIONS_ROLE.md` files include the mandatory budget and session headers.
- [ ] Execution report generated without syntax or file access errors.
