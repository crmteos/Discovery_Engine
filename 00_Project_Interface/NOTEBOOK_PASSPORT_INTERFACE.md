# 📘 NOTEBOOK PASSPORT — INTERFACE (Node 00) — v2.9.0

## 1. Systemic Context & Architecture

| Attribute | Value |
|-----------|-------|
| **Node** | `00_Project_Interface` |
| **Role** | `interface.operator` |
| **Notebook** | Gemini Notebook #1 |
| **System** | Discovery Engine Pipeline v2.9.0 |
| **Budget** | $0.00 (Local Execution) |
| **Message Bus** | `Bridge/messages.jsonl` (Universal Transactional JSONL Bus) |
| **Bus Manager** | `Bridge/bus_manager.py` |
| **Gateway** | `00_Project_Interface/src/anythingllm_gateway.py` |
| **Companion** | `CONTEXT_DOMAIN_INTERFACE.md` (Contextual Data Domain) |
| **Standard** | Notebook Context Standard — Control Plane (2-file notebook context) |

### 1.1 Notebook Context Standard (v2.9.0)

This notebook is the **Architectural Interface (Control Plane)** of Node 00. It governs the `interface.operator` role, the AnythingLLM REST API contract, and the CLI `--payload-file` directive protocol. `CONTEXT_DOMAIN_INTERFACE.md` holds the Data Plane: AnythingLLM workspace sync schemas and dashboard telemetry structures.

### 1.2 Isolation Rule (v2.9.0)

- Node 00 communicates via the universal Message Bus and the registered `interface_to_anythingllm` vector.
- Cross-node Python imports permitted only via manifest-registered paths under `01_Formal_Core/src/`.

## 2. Role Definition

### `interface.operator`

**Responsibilities:**
- Operates the information-interface node: workspace overview, execution reporting, architecture visualization.
- Runs the AnythingLLM GUI Gateway (`anythingllm_gateway.py`) with `--test`, `--sync-workspace`, `--send-chat` flags.
- Accepts Single-Prompt Gateway directives via `Bridge/bus_manager.py --payload-file` and executes them in the Cline session.
- Exposes MCP tools: `architecture_view.py`, `context_view.py`, `anythingllm_gateway.py`, `bus_dashboard.py`.

**Key Capabilities (from `system_manifest.json` v2.9.0):**
- `a2a_agent_card`: role_id `interface.operator`, allowed vectors: `interface_to_master`, `interface_to_bus`, `interface_to_nodes`, `interface_to_anythingllm`, subscriptions: `*`
- `mcp_spec.tools`: `architecture_view.py`, `context_view.py`, `anythingllm_gateway.py`
- `mcp_spec.context_resources`: `system_manifest.json`, `PROJECT_STATE.md`, `Bridge/messages.jsonl`
- `logic_spec_contracts.input_schema`: `00_Project_Interface/schemas/anythingllm_gateway_schema.json`

## 3. Operational Standards

| Standard | Rule | Compliance Check |
|----------|------|------------------|
| **Budget** | $0.00 — pure local execution | `py_compile` exit_code 0 |
| **Gateway** | AnythingLLM `--test` exit_code 0 (fallback mock when server offline) | `--test` exit_code 0 |
| **Message Bus** | `Bridge/bus_manager.py` writes to `Bridge/messages.jsonl` | SHA256 idempotency key |
| **Logic Spec** | Input validated against `anythingllm_gateway_schema.json` | `json.load()` + schema OK |

## 4. Single-Prompt Gateway Protocol (v2.9.0)

1. Architect generates `directive-phaseXX-vX.Y.Z.md` in Studio.
2. Gateway Operator saves it to `Bridge/in/core/directive-phaseXX-vX.Y.Z.md`.
3. Gateway Operator executes Single-Prompt in Cline session (runs `bus_manager.py --post` via `--payload-file` + task execution).
4. Cline executes, updates message status to `completed`, saves execution report to `Bridge/out/execution_reports/`, and returns summary.

## 5. CLI `--payload-file` Protocol

```
python Bridge/bus_manager.py --post --sender system.master_architect \
  --receiver cline.executor --vector vertical --performative task_request \
  --topic directive-phaseXX-vX.Y.Z --payload-file Bridge/in/core/directive-phaseXX-vX.Y.Z.md
```

## 6. Compliance Checklist

- [ ] `anythingllm_gateway.py --test` exit_code 0
- [ ] `json.load()` on `system_manifest.json` PASSED
- [ ] `python test_e2e_pipeline.py` exit_code 0
- [ ] Directive payload-file posted to `Bridge/messages.jsonl` via `bus_manager.py`