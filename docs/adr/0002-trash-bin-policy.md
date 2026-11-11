# ADR 0002 — Trash Bin Policy

## Status
Accepted

## Context
Destructive deletion of files risked losing recoverable artifacts and audit trails.

## Decision
Introduce a non-destructive disposal protocol using `Bridge/trash/`. Files slated for removal are moved to `Bridge/trash/` rather than deleted, preserving recoverability and audit history.

## Consequences
- No permanent data loss on cleanup.
- `scripts/clean_trash.py` manages purging when explicitly requested.