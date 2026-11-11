# ADR 0003 — Single-Prompt Gateway Protocol

## Status
Accepted

## Context
Multi-step manual execution introduced inconsistency and human error.

## Decision
Adopt a 4-step execution workflow exposed through a single-prompt automation interface. Directives are posted to `Bridge/in/` and executed end-to-end by the executor agent, with status updates on the message bus.

## Consequences
- Reproducible, auditable execution.
- Single entry point for all directive-driven work.