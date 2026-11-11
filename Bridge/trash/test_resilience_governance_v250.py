#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discovery Engine v2.5.0 — Resilience & Governance smoke test.
Simulates: DLQ routing, idempotency dedup, circuit breaker trip,
HITL status, semantic gates (NetworkX / SymPy).
"""
import json
import os
import sys

BRIDGE_DIR = r"c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\Bridge"
sys.path.insert(0, BRIDGE_DIR)

import bus_manager  # noqa: E402

BUS_FILE = os.path.join(BRIDGE_DIR, "messages.jsonl")
DLQ_FILE = os.path.join(BRIDGE_DIR, "messages_dlq.jsonl")
STORE_FILE = os.path.join(BRIDGE_DIR, ".idempotency_store.json")

SENDER = "cline.executor"
RECEIVER = "system.master_architect"

VALID_PAYLOAD = {
    "scheme_id": "t-scheme",
    "title": "Test Scheme",
    "keywords": ["smoke"],
    "concepts": [{"name": "cmd", "definition": "no operation"}],
}


def reset_artifacts() -> None:
    for path in (BUS_FILE, DLQ_FILE, STORE_FILE):
        if os.path.exists(path):
            os.remove(path)


def dlq_entries() -> list[dict]:
    if not os.path.exists(DLQ_FILE):
        return []
    with open(DLQ_FILE, "r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def bus_messages() -> list[dict]:
    if not os.path.exists(BUS_FILE):
        return []
    with open(BUS_FILE, "r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


results: list[tuple[str, bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    results.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}".strip())


# --- T1: DLQ routing — unregistered sender → permanent_contract_violation ---
reset_artifacts()
try:
    bus_manager.post_message(
        "unknown.role", RECEIVER, "diagonal", "inform", "t1", {"x": 1}
    )
    check("T1 DLQ routing", False, "no exception raised")
except ValueError as exc:
    entries = dlq_entries()
    perm = [e for e in entries if e["error_type"] == "permanent_contract_violation"]
    check(
        "T1 DLQ routing",
        len(perm) >= 1 and "dlq_reason" in perm[0] and "timestamp" in perm[0],
        f"dlq_records={len(entries)} reason={perm[0]['dlq_reason'][:70] if perm else '-'}",
    )

# --- T2: Idempotency — same (sender, task_id, action_type) twice → one bus message ---
mid1 = bus_manager.post_message(
    SENDER, RECEIVER, "diagonal", "inform", "t2", VALID_PAYLOAD, task_id="task-42", action_type="noop"
)
mid2 = bus_manager.post_message(
    SENDER, RECEIVER, "diagonal", "inform", "t2", VALID_PAYLOAD, task_id="task-42", action_type="noop"
)
msgs = bus_messages()
check("T2 idempotency dedup", mid1 == mid2 and len(msgs) == 1, f"ids={mid1}=={mid2} bus_len={len(msgs)}")
key = bus_manager.compute_idempotency_key(SENDER, "task-42", "noop")
store = json.load(open(STORE_FILE, "r", encoding="utf-8"))
check("T2 store completed", store.get(key, {}).get("status") == "completed", f"store={store.get(key)}")

# --- T3: Circuit breaker — hop_count 4 > max_hops 3 ---
try:
    bus_manager.post_message(
        SENDER, RECEIVER, "diagonal", "inform", "t3", VALID_PAYLOAD, hop_count=4
    )
    check("T3 circuit breaker", False, "no exception raised")
except ValueError as exc:
    entries = dlq_entries()
    circ = [e for e in entries if e["error_type"] == "circuit_breaker"]
    check(
        "T3 circuit breaker",
        len(circ) >= 1,
        f"circuit_records={len(circ)} reason={circ[0]['dlq_reason'][:70] if circ else '-'}",
    )

# --- T4: Semantic gate — cyclic graph via NetworkX ---
try:
    bus_manager.post_message(
        SENDER,
        RECEIVER,
        "diagonal",
        "inform",
        "t4",
        {"graph": {"nodes": ["a", "b"], "edges": [
            {"source": "a", "target": "b"}, {"source": "b", "target": "a"}
        ]}, **VALID_PAYLOAD},
    )
    check("T4 semantic gate", False, "no exception raised")
except ValueError as exc:
    entries = dlq_entries()
    sem = [e for e in entries if e["error_type"] == "semantic_invariant_violation"]
    check(
        "T4 semantic gate",
        len(sem) >= 1,
        f"sem_records={len(sem)} reason={sem[0]['dlq_reason'][:70] if sem else '-'}",
    )

# --- T5: Semantic gate — inconsistent SymPy assertion ---
try:
    bus_manager.post_message(
        SENDER, RECEIVER, "diagonal", "inform", "t5",
        {"logic_assertions": ["not_a_valid_expression@@@"], **VALID_PAYLOAD},
    )
    check("T5 sympy gate", False, "no exception raised")
except ValueError as exc:
    check("T5 sympy gate", True, f"reason={str(exc)[:70]}")

# --- T6: HITL — human_approval_required → awaiting_human_approval ---
mid6 = bus_manager.post_message(
    SENDER,
    "cline.executor",
    "diagonal",
    "human_approval_required",
    "target_model_build",
    {"stage": "06_Formalized_Model"},
)
m6 = [m for m in bus_messages() if m["id"] == mid6]
check("T6 HITL status", bool(m6) and m6[0]["status"] == "awaiting_human_approval",
      f"status={m6[0]['status'] if m6 else '-'}")

# --- T7: Valid message still posts normally ---
mid7 = bus_manager.post_message(SENDER, RECEIVER, "diagonal", "inform", "t7", VALID_PAYLOAD)
check("T7 valid post", mid7 is not None and len(bus_messages()) >= 1, f"msg_id={mid7}")

# --- Summary ---
fails = [r for r in results if not r[1]]
print("\n=== RESILIENCE GOVERNANCE v2.5.0 SMOKE TEST ===")
print(f"Passed: {len(results) - len(fails)}/{len(results)}")
for name, ok, detail in results:
    if not ok:
        print(f"  FAILED: {name} — {detail}")
sys.exit(1 if fails else 0)
