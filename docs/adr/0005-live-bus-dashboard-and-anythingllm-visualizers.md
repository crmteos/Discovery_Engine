# ADR 0005 — Live Bus Dashboard & AnythingLLM Visualizer Integration

- Status: Accepted
- Date: 2026-11-10

## Context
Node 00 needed live observability into Bridge/messages.jsonl and publishing to AnythingLLM.

## Decision
- Add bus_dashboard.py with --cli, --export-md, --export-svg.
- Extend anythingllm_gateway.py with --sync-dashboard.
- Update passports, manifest to v3.3.0.

## Consequences
- Continuous observability and visualizer sync.