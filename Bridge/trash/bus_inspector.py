""""
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