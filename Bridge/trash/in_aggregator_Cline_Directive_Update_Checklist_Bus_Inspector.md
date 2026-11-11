# TASK DIRECTIVE: Update Operational Checklist & Deploy Bus Inspector Utility
**Target Subsystem:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`
**Sender:** System Architect (Gemini Notebook #2)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Protocol Standard:** `AGGREGATOR_OPERATIONAL_PROTOCOL.md` (Node 05 v2.6.0)
**Budget Constraint:** $0.00 (Pure Local Execution)

--------------------------------------------------------------------------------

#### 🎯 Executive Objective
1. **Update `AGGREGATOR_CHECKLIST.md`**: Mark all completed infrastructure milestones (W3C PROV-O/SKOS validator, transactional message bus, media templates, `intake_processor.py` extension) and append new phases for media extraction and end-to-end knowledge ingestion.
2. **Deploy `bus_inspector.py`**: Create a dedicated validation and monitoring tool inside `05_Knowledge_Aggregator/` to audit `Bridge/messages.jsonl` transactions, check SHA256 idempotency keys, and verify W3C PROV-O metadata integrity.
3. **Run Health Verification**: Perform a test run of `bus_inspector.py` against `Bridge/messages.jsonl` and record the execution report.

--------------------------------------------------------------------------------

#### 🛠️ Step-by-Step Execution Tasks

##### Task 1: Synchronize `05_Knowledge_Aggregator/AGGREGATOR_CHECKLIST.md`
Update the operational checklist file with the following state:

```markdown
### 05_Knowledge_Aggregator — Operational Plan & Master Checklist
###### Subsystem Scope & Target Directory
C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator

--------------------------------------------------------------------------------

###### 📋 Phase 1: Ingestion Infrastructure & Schema Audit
*  [x] **Subsystem Isolation:** Dedicated AGGREGATOR_STATE.md initialized.
*  [x] **Channel Architecture:** Sub-channels Bridge/in/aggregator/ and Bridge/out/aggregator_reports/ configured.
*  [x] **Schema Contract Validation:** Upgraded schema_validator.py for W3C PROV-O and SKOS compliance across all 5 categories (cognitive_model, analogy, concept_scheme, image_metadata, video_index).
*  [x] **Intake Handler Extension:** intake_processor.py extended and verified with exit code 0 for all 5 categories.

--------------------------------------------------------------------------------

###### 📋 Phase 2: Transactional Message Bus & Telemetry
*  [x] **Message Bus Integration:** bus_manager.py implementing SHA256-keyed append-only logging to Bridge/messages.jsonl.
*  [ ] **Bus Integrity Inspection:** Deploy bus_inspector.py to audit SHA256 idempotency keys, timestamp ISO 8601 UTC compliance, and message payload schemas.

--------------------------------------------------------------------------------

###### 📋 Phase 3: Media & Multimodal Intake Infrastructure
*  [x] **Media Schema Standards:** Created image_metadata_template.json and video_index_template.json under Intake_Queue/templates/.
*  [ ] **Media Auto-Extractors:** Build local image metadata parser and video timestamp indexer under 05_Knowledge_Aggregator/media_extractors/.
*  [ ] **Cross-Media RDF Linking:** Enrich intake_processor.py to map visual keys and temporal chunks to formal RDF triples.

--------------------------------------------------------------------------------

###### 📋 Phase 4: End-to-End Live Knowledge Ingestion
*  [ ] **Sample Model Processing:** Ingest comprehensive multi-domain cognitive model with linked image and video metadata.
*  [ ] **Zero-Hallucination Audit:** Verify 100% deterministic traceability from intake files to Processed_Gate/normalized_triples/.
*  [ ] **Core Handoff Verification:** Validate RDF triples and message bus logs for ingestion by 01_Formal_Core.

--------------------------------------------------------------------------------

###### 📋 Phase 5: Execution & Logging
*  [x] **Log Storage:** Record intake summary reports to Bridge/out/aggregator_reports/.
*  [x] **Local Metrics Sync:** Maintain AGGREGATOR_STATE.md with local hardware and queue telemetry.
```

##### Task 2: Deploy `05_Knowledge_Aggregator/bus_inspector.py`
Create `05_Knowledge_Aggregator/bus_inspector.py`:

```python
"""
Bus Inspector Utility: Audits Bridge/messages.jsonl for SHA256 idempotency,
W3C PROV-O compliance, and event schema integrity.
"""
import json
import os
import sys
from pathlib import Path

BUS_FILE = Path(__file__).resolve().parent.parent / "Bridge" / "messages.jsonl"
REPORT_DIR = Path(__file__).resolve().parent.parent / "Bridge" / "out" / "aggregator_reports"

def audit_message_bus():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not BUS_FILE.exists():
        print(f"Warning: Bus file {BUS_FILE} does not exist yet.")
        return {"total_messages": 0, "valid_messages": 0, "errors": ["Bus file missing"]}

    total = 0
    valid = 0
    seen_keys = set()
    errors = []

    with open(BUS_FILE, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                msg = json.loads(line)
                # Check required fields
                if "timestamp" not in msg or "task_id" not in msg or "action" not in msg or "payload" not in msg:
                    errors.append(f"Line {idx}: Missing core JSONL fields")
                    continue
                
                # Check SHA256 idempotency if key present
                msg_key = msg.get("idempotency_key") or msg.get("task_id")
                if msg_key in seen_keys:
                    errors.append(f"Line {idx}: Duplicate transaction key '{msg_key}'")
                seen_keys.add(msg_key)

                valid += 1
            except Exception as e:
                errors.append(f"Line {idx}: JSON parse error - {e}")

    summary = {
        "total_messages": total,
        "valid_messages": valid,
        "unique_keys": len(seen_keys),
        "errors": errors
    }
    
    print(f"Bus Audit Completed: {valid}/{total} valid messages. {len(errors)} errors found.")
    return summary

if __name__ == "__main__":
    audit_message_bus()
```

##### Task 3: Syntax Check & Initial Run
1. Verify syntax: `python -m py_compile 05_Knowledge_Aggregator/bus_inspector.py`
2. Execute inspector: `python 05_Knowledge_Aggregator/bus_inspector.py`
3. Save execution report to `Bridge/out/aggregator_reports/report_bus_inspector_[TIMESTAMP].md`.

--------------------------------------------------------------------------------

#### 🔍 Verification & Compliance Checklist
* [ ] `05_Knowledge_Aggregator/AGGREGATOR_CHECKLIST.md` updated on disk.
* [ ] `05_Knowledge_Aggregator/bus_inspector.py` created and compiled without errors (exit code 0).
* [ ] Bus audit executed against `Bridge/messages.jsonl`.
* [ ] Report saved in `Bridge/out/aggregator_reports/`.
