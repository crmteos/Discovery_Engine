# 🗄️ CONTEXT DOMAIN — INTERFACE (Node 00) — v2.9.0

## 1. Systemic Context & Data Domain

| Attribute | Value |
|-----------|-------|
| **Node** | `00_Project_Interface` |
| **Domain** | AnythingLLM workspace sync schemas, dashboard telemetry structures |
| **Notebook** | Gemini Notebook #1 |
| **System** | Discovery Engine Pipeline v2.9.0 |
| **Budget** | $0.00 (Local Execution) |
| **Companion** | `NOTEBOOK_PASSPORT_INTERFACE.md` (Architectural / Control Plane) |
| **Standard** | Notebook Context Standard — Data Plane (2-file notebook context) |

## 2. Purpose

This notebook is the **Contextual Data Domain (Data Plane)** of Node 00. It defines the AnythingLLM workspace synchronization schemas, the dashboard telemetry structures, and the governance contract schemas used by the `interface.operator` role and the AnythingLLM GUI Gateway.

## 3. Schemas & Contracts (`00_Project_Interface/schemas/`)

### 3.1 AnythingLLM Gateway Schema (`anythingllm_gateway_schema.json`)

Logic-Spec input schema for `interface.operator`. Validates directive payloads submitted through the AnythingLLM gateway:
- `meta` / `metadata`, `type`, `version`, and one of `entities` / `source_domain` / `nodes`.
- Directive envelope: `topic`, `performative`, `sender`, `receiver`, `payload-file`.

### 3.2 Workspace Sync Schemas

- AnythingLLM workspace sync structures (local mirror of workspace state).
- Dashboard telemetry structures: execution counts, node statuses, phase milestones, budget telemetry ($0.00).

## 4. Dashboard Telemetry Structures

| Telemetry Field | Description | Source |
|-----------------|-------------|--------|
| `execution_count` | Number of executed directives | `Bridge/messages.jsonl` |
| `node_status` | Per-node readiness (🟢/🟡/🔴) | `system_manifest.json` nodes |
| `phase_milestone` | Latest completed phase | `PROJECT_STATE.md` Execution History |
| `budget` | Current budget (USD) | $0.00 fixed |
| `system_readiness` | Overall core readiness | `PROJECT_STATE.md` header metrics |

## 5. Data Flow

```
Directive (Bridge/in/core/*.md)
    → bus_manager.py --post --payload-file
    → Bridge/messages.jsonl (append-only JSONL bus)
    → cline.executor executes task
    → Execution report (Bridge/out/execution_reports/)
    → Dashboard telemetry updated
```

## 6. Compliance Checklist

- [ ] `anythingllm_gateway_schema.json` valid JSON (`json.load()` OK)
- [ ] Workspace sync schemas present under `00_Project_Interface/schemas/`
- [ ] Dashboard telemetry structures reference `Bridge/messages.jsonl`