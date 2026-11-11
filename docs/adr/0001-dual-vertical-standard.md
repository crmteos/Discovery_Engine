# ADR 0001 — Dual-Vertical Standard

## Status
Accepted

## Context
The Discovery Engine historically mixed governance/control concerns with domain knowledge in single files, making maintenance and evolution difficult.

## Decision
Adopt a Dual-Vertical Standard splitting the system into:
- **Control Plane (Governance)**: `PROJECT_STATE.md` — authoritative state, metrics, execution history.
- **Data Plane (Domain Knowledge)**: `PROJECT_CONTEXT.md` — domain knowledge and context.

## Consequences
- Clearer separation of concerns.
- Independent evolution of governance and knowledge planes.
- All agents must read both planes before execution.