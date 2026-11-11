#!/usr/bin/env python3
"""model_bus_listener.py - Interface for reading messages.jsonl for role: model.builder."""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

MESSAGES_PATH = Path("Bridge/messages.jsonl")


def load_messages(receiver: str = "model.builder") -> List[Dict]:
    """Load messages from the universal message bus filtered by receiver."""
    messages = []
    path = Path("Bridge/messages.jsonl")
    if not path.exists():
        return messages
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg_receiver = msg.get("receiver") or msg.get("to") or ""
            if msg_receiver == receiver or msg.get("role") == receiver:
                messages.append(msg)
    return messages


def get_pending_tasks() -> List[Dict]:
    """Query pending tasks from the message bus."""
    msgs = load_messages("model.builder")
    tasks = [m for m in msgs if m.get("type") in ("task", "directive", "command")]
    return tasks


def get_core_hypotheses() -> List[Dict]:
    """Display incoming Core hypotheses (HYPOTHESIS_*)."""
    msgs = load_messages("model.builder")
    hypotheses = [m for m in msgs if m.get("content", "").startswith("HYPOTHESIS_")]
    return hypotheses


def send_response(message: Dict) -> bool:
    """Send a response message back to the bus."""
    path = Path("Bridge/messages.jsonl")
    try:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
        return True
    except Exception as e:
        print(f"Error sending response: {e}", file=sys.stderr)
        return False


def list_pending() -> None:
    """CLI method to list all pending tasks from the bus."""
    tasks = get_pending_tasks()
    if not tasks:
        print("No pending tasks found for model.builder.")
        return
    for i, task in enumerate(tasks, 1):
        print(f"{i}. ID: {task.get('id', 'N/A')}")
        print(f"   Role: {task.get('role', 'N/A')}")
        print(f"   Content: {task.get('content', '')[:100]}...")
        print()


def list_hypotheses() -> None:
    """CLI method to display incoming Core hypotheses."""
    hypotheses = get_core_hypotheses()
    if not hypotheses:
        print("No Core hypotheses found.")
        return
    for i, hyp in enumerate(hypotheses, 1):
        print(f"{i}. ID: {hyp.get('id', 'N/A')}")
        print(f"   Content: {hyp.get('content', '')[:200]}...")
        print()
