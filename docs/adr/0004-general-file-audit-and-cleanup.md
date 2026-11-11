# ADR 0004: General Codebase Audit, File Standardization and Trash Archival

**Status:** Accepted

**Context:** Project growth led to residual files and minor layout drift.

**Decision:** All nodes strictly enforce 2-file envelopes, root contains only core governance manifests, obsolete files are archived to `Bridge/trash/`.
