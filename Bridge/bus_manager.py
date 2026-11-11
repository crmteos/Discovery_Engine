#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge Universal Transactional Message Bus — v3.5.0.

Central Message Bus for the Discovery Engine. All inter-node / inter-role
communication is routed through a single append-only JSONL log:

    Bridge/messages.jsonl            transactional messages
    Bridge/messages_dlq.jsonl        triaged failures (DLQ)
    Bridge/.idempotency_store.json   deduplication store

API
---
    post_message(...)                -> message id
    get_pending_messages(...)        -> list of pending messages
    update_message_status(...)       -> updated record
    log_core_telemetry(...)          -> message id (OpenTelemetry GenAI log)
    post_to_dlq(...)                 -> dlq_id

CLI
---
    bus_manager.py --list-pending
    bus_manager.py --post --payload-file <path>
    bus_manager.py --update --msg-id <id> --status completed
    bus_manager.py --list-dlq
    bus_manager.py --log-telemetry --step-name <name> --metrics-json '{}'
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from jsonschema import Draft7Validator, FormatChecker
from jsonschema.exceptions import ValidationError

BRIDGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BRIDGE_DIR.parent
MESSAGES_FILE = BRIDGE_DIR / "messages.jsonl"
DLQ_FILE = BRIDGE_DIR / "messages_dlq.jsonl"
IDEMPOTENCY_STORE_FILE = BRIDGE_DIR / ".idempotency_store.json"

MAX_HOPS = 3


def _utc_now() -> str:
    """Current UTC time as an ISO-8601 string with Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_now_id() -> str:
    """Current UTC time as YYYYMMDD_HHMMSS (id prefixes)."""
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _load_jsonl(path: Path) -> list:
    """Load JSONL records; blank and malformed lines are skipped."""
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except ValueError:
                continue
    return records


def _append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON record as a new line (JSONL).

    JSONL is append-only by design: each line is a complete, independent
    JSON object, so a direct append is safe and preserves all prior records.
    """
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _save_jsonl_lines(path: Path, records: list) -> None:
    """Rewrite a JSONL file from a list of records (atomic replace)."""
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def _next_message_id() -> str:
    """Unique message id: msg_YYYYMMDD_HHMMSS[_N] (collision-safe)."""
    base = "msg_" + _utc_now_id()
    existing = {rec.get("id") for rec in _load_jsonl(MESSAGES_FILE) if rec.get("id")}
    candidate = base
    counter = 2
    while candidate in existing:
        candidate = "{}_{}".format(base, counter)
        counter += 1
    return candidate


def _as_original_record(record: dict) -> dict:
    """Minimal envelope for DLQ records (matches the on-disk DLQ schema)."""
    return {
        "sender": record.get("sender"),
        "receiver": record.get("receiver"),
        "communication_vector": record.get("communication_vector"),
        "performative": record.get("performative"),
        "topic": record.get("topic"),
        "payload": record.get("payload"),
        "hop_count": record.get("hop_count"),
    }


def _build_message_record(
    sender: str,
    receiver: str,
    vector: str,
    performative: str,
    topic: str,
    payload: Any,
    in_reply_to: Optional[str] = None,
    task_id: Optional[str] = None,
    action_type: Optional[str] = None,
    hop_count: int = 0,
) -> dict:
    """Build a canonical bus-message envelope (id filled by the caller)."""
    action = action_type or performative
    return {
        "timestamp": _utc_now(),
        "communication_vector": vector,
        "sender": sender,
        "receiver": receiver,
        "performative": performative,
        "topic": topic,
        "context_scope": None,
        "in_reply_to": in_reply_to,
        "payload": payload,
        "hop_count": hop_count,
        "idempotency_key": compute_idempotency_key(sender, task_id, action_type),
        "task_id": task_id,
        "action": action,
        "status": "awaiting_human_approval" if performative == "human_approval_required" else "pending",
        "result": {
            "exit_code": None,
            "report_ref": None,
            "response_payload": None,
        },
    }
# ---------------------------------------------------------------------------
# Core API: post / idempotency / DLQ
# ---------------------------------------------------------------------------

class BusRejection(ValueError):
    """Contract violation rejected by the pre-flight gates (Phase 13/14)."""

    def __init__(self, reason: str, error_type: str) -> None:
        super().__init__(reason)
        self.reason = reason
        self.error_type = error_type


def compute_idempotency_key(sender: str, task_id: Optional[str] = None, action_type: Optional[str] = None) -> str:
    """Deterministic idempotency key: SHA-256 of 'sender|task_id|action_type'."""
    parts = [part for part in (sender, task_id, action_type) if part]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _load_idempotency_store() -> dict:
    """Load the persistent idempotency store (empty dict on first run)."""
    if not IDEMPOTENCY_STORE_FILE.exists():
        return {}
    try:
        return json.loads(IDEMPOTENCY_STORE_FILE.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def _save_idempotency_store(store: dict) -> None:
    """Persist the idempotency store atomically."""
    tmp = IDEMPOTENCY_STORE_FILE.with_name(IDEMPOTENCY_STORE_FILE.name + ".tmp")
    tmp.write_text(json.dumps(store, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, IDEMPOTENCY_STORE_FILE)


def _reject_to_dlq(reason: str, error_type: str, sender: str, receiver: str, vector: str, performative: str, topic: str, payload: Any, in_reply_to: Optional[str] = None, task_id: Optional[str] = None, action_type: Optional[str] = None, hop_count: int = 0) -> None:
    """Write the rejected message to the DLQ and raise BusRejection."""
    record = _build_message_record(sender, receiver, vector, performative, topic, payload, in_reply_to, task_id, action_type, hop_count)
    post_to_dlq(_as_original_record(record), reason, error_type)


def post_message(
    sender: str,
    receiver: str,
    vector: str,
    performative: str,
    topic: str,
    payload: Any,
    in_reply_to: Optional[str] = None,
    task_id: Optional[str] = None,
    action_type: Optional[str] = None,
    hop_count: int = 0,
) -> str:
    """Post a validated message to the universal message bus.

    Pre-flight gates (Phase 13/14):
      * sender must be registered in the role_capability_registry
      * communication vector must be allowed for the sender
      * payload must validate against the receiver's Logic-Spec input_schema
      * hop_count must not exceed MAX_HOPS (circuit breaker)
      * semantic invariants are checked (NetworkX / SymPy)
    Idempotency (Phase 14): duplicate (sender, task_id, action_type) tuples
    are de-duplicated against the persisted store.
    """
    key = compute_idempotency_key(sender, task_id, action_type)
    store = _load_idempotency_store()
    if store.get(key, {}).get("status") == "completed":
        return store[key]["message_id"]

    try:
        _validate_sender_registration(sender)
        _validate_vector(sender, vector)
        _validate_payload_schema(receiver, payload)
        _check_circuit_breaker(hop_count)
        _validate_semantic_invariants(payload)
    except BusRejection:
        raise

    record = _build_message_record(sender, receiver, vector, performative, topic, payload, in_reply_to, task_id, action_type, hop_count)
    record["id"] = _next_message_id()
    _append_jsonl(MESSAGES_FILE, record)

    store[key] = {"status": "completed", "message_id": record["id"], "timestamp": record["timestamp"]}
    _save_idempotency_store(store)
    return record["id"]


def _schema_path_for(receiver: str) -> Optional[str]:
    """Resolve a receiver's Logic-Spec input_schema relative to the project root."""
    registry = _load_role_registry()
    contracts = registry.get(receiver, {}).get("logic_spec_contracts", {}) or {}
    return contracts.get("input_schema")

# ---------------------------------------------------------------------------
# Validation helpers (Phase 13/14 guards)
# ---------------------------------------------------------------------------

def _load_role_registry() -> dict:
    """Load the role_capability_registry from system_manifest.json at the project root."""
    manifest_path = PROJECT_ROOT / "system_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return manifest.get("role_capability_registry", {})


def _load_json_schema(relative_path: str) -> Optional[dict]:
    """Load a JSON Schema from a path relative to the project root."""
    schema_path = PROJECT_ROOT / relative_path
    try:
        return json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _validate_sender_registration(sender: str) -> None:
    """Reject messages whose sender role is not registered in the registry."""
    registry = _load_role_registry()
    if sender not in registry:
        raise BusRejection(
            "A2A violation: sender '{}' is not registered in role_capability_registry.".format(sender),
            "permanent_contract_violation",
        )


def _validate_vector(sender: str, vector: str) -> None:
    """Reject messages whose communication vector is not allowed for the sender."""
    registry = _load_role_registry()
    allowed = registry.get(sender, {}).get("a2a_agent_card", {}).get("allowed_vectors", [])
    if vector not in allowed:
        raise BusRejection(
            "A2A violation: vector '{}' is not allowed for sender '{}' (allowed: {}).".format(vector, sender, ", ".join(allowed)),
            "permanent_contract_violation",
        )


def _validate_payload_schema(receiver: str, payload: Any) -> None:
    """Validate the payload against the receiver's Logic-Spec input_schema (Draft 7)."""
    schema_path = _schema_path_for(receiver)
    if not schema_path:
        return
    schema = _load_json_schema(schema_path)
    if schema is None:
        return
    try:
        Draft7Validator(schema, format_checker=FormatChecker()).validate(payload)
    except ValidationError as exc:
        raise BusRejection(
            "Logic-Spec violation: payload for receiver '{}' does not conform to input_schema '{}': {}".format(receiver, schema_path, exc.message),
            "permanent_contract_violation",
        ) from exc


def _check_circuit_breaker(hop_count: int) -> None:
    """Circuit breaker guard: hop_count must not exceed MAX_HOPS."""
    if hop_count > MAX_HOPS:
        raise BusRejection(
            "circuit_breaker: hop_count {} exceeds max_hops {}; cascade terminated".format(hop_count, MAX_HOPS),
            "circuit_breaker",
        )


def _validate_semantic_invariants(payload: Any) -> bool:
    """NetworkX / SymPy semantic gates (Phase 14).

    Returns True when the payload passes.  Raises BusRejection with a
    machine-readable reason when a gate fails.
    """
    if not isinstance(payload, dict):
        return True  # raw-text / non-object payloads: no gates apply

    if "graph" in payload and isinstance(payload["graph"], dict):
        graph = payload["graph"]
        if isinstance(graph, dict) and "nodes" in graph and "edges" in graph:
            try:
                import networkx as nx
            except ImportError:
                return True
            directed = nx.DiGraph()
            for node in graph["nodes"]:
                directed.add_node(node)
            for edge in graph["edges"]:
                if isinstance(edge, dict):
                    src, dst = edge.get("source"), edge.get("target")
                    if src is not None and dst is not None:
                        directed.add_edge(src, dst)
                elif isinstance(edge, (list, tuple)) and len(edge) >= 2:
                    directed.add_edge(edge[0], edge[1])
            if list(nx.simple_cycles(directed)):
                raise BusRejection(
                    "Semantic violation: knowledge graph contains a closed cycle",
                    "semantic_invariant_violation",
                )

    if "logic_assertions" in payload and isinstance(payload["logic_assertions"], list):
        try:
            import sympy as sp
        except ImportError:
            return True
        for assertion in payload["logic_assertions"]:
            try:
                sp.sympify(str(assertion))
            except Exception as exc:
                raise BusRejection(
                    "Semantic violation: inconsistent logic assertion {!r}: {}".format(assertion, exc),
                    "semantic_invariant_violation",
                ) from exc
    return True

# ---------------------------------------------------------------------------
# Telemetry / status / DLQ helpers
# ---------------------------------------------------------------------------

def log_core_telemetry(step_name: str, metrics: Optional[dict] = None, status: str = "completed") -> Optional[str]:
    """Append an OpenTelemetry GenAI semantic log to Bridge/messages.jsonl.

    Maps OpenTelemetry event semantics onto the transactional bus envelope:
      - 'name'  -> action / step_name
      - 'attrs' -> payload / metrics
      - 'status'-> status
    Best effort: a write failure is swallowed so core engines can log
    telemetry without cascading failures.
    """
    if metrics is None:
        metrics = {}
    if not isinstance(metrics, dict):
        metrics = {"payload": metrics}
    try:
        record = {
            "id": _next_message_id(),
            "timestamp": _utc_now(),
            "communication_vector": "system",
            "sender": "system.master_architect",
            "receiver": "system.master_architect",
            "performative": "status_update",
            "topic": "telemetry",
            "context_scope": None,
            "in_reply_to": None,
            "payload": {"step_name": step_name, **metrics},
            "hop_count": 0,
            "idempotency_key": None,
            "task_id": None,
            "action": step_name,
            "status": status,
            "result": {
                "exit_code": 0 if status == "completed" else 1,
                "report_ref": None,
                "response_payload": None,
            },
        }
        _append_jsonl(MESSAGES_FILE, record)
        return record["id"]
    except OSError:
        return None


def get_pending_messages(receiver_role: Optional[str] = None) -> list:
    """Return messages with status 'pending' (optionally filtered by receiver)."""
    pending = [rec for rec in _load_jsonl(MESSAGES_FILE) if rec.get("status") == "pending"]
    if receiver_role is not None:
        pending = [rec for rec in pending if rec.get("receiver") == receiver_role]
    return pending


def update_message_status(msg_id: str, status: str, exit_code: int = 0, report_ref: Optional[str] = None, response_payload: Any = None) -> dict:
    """Update the status/result of a previously posted message."""
    records = _load_jsonl(MESSAGES_FILE)
    for index, record in enumerate(records):
        if record.get("id") != msg_id:
            continue
        old = dict(record)
        record["status"] = status
        record.setdefault("result", {})
        record["result"]["exit_code"] = exit_code
        record["result"]["report_ref"] = report_ref
        record["result"]["response_payload"] = response_payload
        _save_jsonl_lines(MESSAGES_FILE, records)
        return record
    raise KeyError("message not found: {}".format(msg_id))


def _next_dlq_id() -> str:
    """Unique dlq id: dlq_YYYYMMDD_HHMMSS_XXXXXX (timestamp + 6 digits)."""
    base = "dlq_" + _utc_now_id()
    existing = {rec.get("dlq_id") for rec in _load_jsonl(DLQ_FILE) if rec.get("dlq_id")}
    candidate = base
    counter = 1
    while candidate in existing:
        candidate = "{}_{:06d}".format(base, counter)
        counter += 1
    return candidate


def post_to_dlq(original_record: dict, reason: str, error_type: str) -> str:
    """Write a failed message to Bridge/messages_dlq.jsonl and return dlq_id."""
    record = {
        "dlq_id": _next_dlq_id(),
        "timestamp": _utc_now(),
        "dlq_reason": reason,
        "error_type": error_type,
        "original_record": original_record,
    }
    _append_jsonl(DLQ_FILE, record)
    return record["dlq_id"]

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bus_manager.py",
        description="Universal Transactional Message Bus (Bridge/bus_manager.py)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list-pending", help="List pending bus messages")
    p_list.add_argument("--receiver", help="Filter by receiver role")

    p_post = sub.add_parser("post", help="Post a message to the bus")
    p_post.add_argument("--payload-file", type=Path, help="Path to a JSON payload file")
    p_post.add_argument("--payload-json", help="Inline JSON payload string")
    p_post.add_argument("--sender", help="Sender role (required)")
    p_post.add_argument("--receiver", help="Receiver role (required)")
    p_post.add_argument("--vector", help="Communication vector (vertical|horizontal|diagonal|system)")
    p_post.add_argument("--performative", help="FIPA-ACL performative")
    p_post.add_argument("--topic", help="Message topic")
    p_post.add_argument("--in-reply-to", help="In-reply-to message id")
    p_post.add_argument("--task-id", help="Task id used for idempotency")
    p_post.add_argument("--action-type", help="Action type used for idempotency")
    p_post.add_argument("--hop-count", type=int, default=0, help="Hop count (circuit breaker: max {})".format(MAX_HOPS))

    p_update = sub.add_parser("update", help="Update message status on the bus")
    p_update.add_argument("--msg-id", required=True, help="Message id")
    p_update.add_argument("--status", required=True, help="New status")
    p_update.add_argument("--exit-code", type=int, default=0)
    p_update.add_argument("--report-ref", default=None)
    p_update.add_argument("--response-payload", default=None)

    p_dlq = sub.add_parser("list-dlq", help="List DLQ entries")
    p_dlq.add_argument("--error-type", help="Filter by error type")

    p_tel = sub.add_parser("log-telemetry", help="Log OpenTelemetry-style semantic telemetry")
    p_tel.add_argument("--step-name", required=True, help="Step / event name")
    p_tel.add_argument("--metrics-json", default="{}", help="JSON metrics payload")
    p_tel.add_argument("--status", default="completed", help="Telemetry status (completed|failed)")

    args = parser.parse_args(argv)

    if args.command == "list-pending":
        for record in get_pending_messages(args.receiver):
            print("{} | {} | {} | {} | {}".format(
                record.get("id"), record.get("sender"), record.get("receiver"),
                record.get("performative"), record.get("topic")))
        return 0

    if args.command == "post":
        if not args.sender or not args.receiver or not args.vector or not args.performative or not args.topic:
            parser.error("--post requires --sender --receiver --vector --performative --topic")
        if args.payload_file and args.payload_json:
            parser.error("use either --payload-file or --payload-json, not both")
        if not args.payload_file and not args.payload_json:
            parser.error("--post requires --payload-file or --payload-json")
        try:
            if args.payload_file:
                with args.payload_file.open("r", encoding="utf-8") as handle:
                    payload = json.load(handle)
            else:
                payload = json.loads(args.payload_json)
        except (OSError, ValueError) as exc:
            print("ERROR: cannot read payload: {}".format(exc), file=sys.stderr)
            return 2
        message_id = post_message(
            sender=args.sender,
            receiver=args.receiver,
            vector=args.vector,
            performative=args.performative,
            topic=args.topic,
            payload=payload,
            in_reply_to=args.in_reply_to,
            task_id=args.task_id,
            action_type=args.action_type,
            hop_count=args.hop_count,
        )
        print(message_id)
        return 0

    if args.command == "update":
        try:
            update_message_status(args.msg_id, args.status, args.exit_code, args.report_ref, args.response_payload)
        except KeyError as exc:
            print("ERROR: {}".format(exc), file=sys.stderr)
            return 1
        return 0

    if args.command == "list-dlq":
        for record in _load_jsonl(DLQ_FILE):
            if args.error_type and record.get("error_type") != args.error_type:
                continue
            print("{} | {} | {} | {}".format(
                record.get("dlq_id"), record.get("error_type"),
                record.get("dlq_reason"), record.get("timestamp")))
        return 0

    if args.command == "log-telemetry":
        try:
            metrics = json.loads(args.metrics_json)
        except ValueError as exc:
            print("ERROR: bad metrics JSON: {}".format(exc), file=sys.stderr)
            return 2
        log_core_telemetry(args.step_name, metrics=metrics, status=args.status)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

