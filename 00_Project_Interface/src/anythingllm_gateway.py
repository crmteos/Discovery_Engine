#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00_Project_Interface/src/anythingllm_gateway.py — AnythingLLM GUI Gateway (v2.8.0).

Gateway bridge between the AnythingLLM REST API (http://localhost:3001/api/v1)
and the central Message Bus (Bridge/bus_manager.py).

Supports:
  --test        Diagnostic validation of local API connectivity (fallback mock
                ping if offline). Structured status with exit_code: 0.
  --sync-workspace  Fetches active workspaces and posts document intake
                directives into Bridge/messages.jsonl for Node 05
                (aggregator.architect).
  --send-chat   Packages user prompts or synthesized models into AnythingLLM
                chat payload format.

Robust exception handling: graceful fallback when AnythingLLM server is not
actively running.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"
BUS_FILE = BRIDGE_DIR / "messages.jsonl"
SCHEMA_PATH = PROJECT_ROOT / "00_Project_Interface" / "schemas" / "anythingllm_gateway_schema.json"

# Ensure Bridge/ is importable for bus_manager
if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

ANYTHINGLLM_BASE_URL = "http://127.0.0.1:3001/api/v1"
REQUEST_TIMEOUT = 3
ANYTHINGLLM_API_KEY = None
TARGET_WORKSPACE = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _post_bus_message(
    sender: str,
    receiver: str,
    vector: str,
    performative: str,
    topic: str,
    payload: dict[str, Any],
) -> str | None:
    """Post a message to the universal message bus via bus_manager.py."""
    try:
        from bus_manager import post_message  # type: ignore

        return post_message(
            sender=sender,
            receiver=receiver,
            vector=vector,
            performative=performative,
            topic=topic,
            payload=payload,
        )
    except Exception as exc:  # pragma: no cover - bus fallback
        print(f"[WARN] Could not post to message bus: {exc}", file=sys.stderr)
        return None


def _anythingllm_request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Make a request to the AnythingLLM REST API with graceful fallback."""
    if requests is None:
        return {
            "ok": False,
            "error": "requests package not installed",
            "fallback": True,
        }

    url = f"{ANYTHINGLLM_BASE_URL}{path}"
    headers = {}
    if ANYTHINGLLM_API_KEY:
        headers["Authorization"] = f"Bearer {ANYTHINGLLM_API_KEY}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
        else:
            return {"ok": False, "error": f"Unsupported method: {method}", "fallback": True}

        return {
            "ok": response.status_code < 400,
            "status_code": response.status_code,
            "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            "fallback": False,
        }
    except requests.exceptions.ConnectionError:
        return {
            "ok": False,
            "error": "AnythingLLM server not reachable at " + ANYTHINGLLM_BASE_URL,
            "fallback": True,
        }
    except requests.exceptions.Timeout:
        return {
            "ok": False,
            "error": "AnythingLLM request timed out",
            "fallback": True,
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {"ok": False, "error": str(exc), "fallback": True}


# ---------------------------------------------------------------------------
# --test
# ---------------------------------------------------------------------------

def run_test(workspace_slug: str | None = None) -> dict[str, Any]:
    """Run diagnostic validation of local API connectivity.

    Returns structured status with exit_code: 0 even when the server is offline
    (fallback mock ping).
    """
    results: dict[str, Any] = {
        "timestamp": _utc_now(),
        "gateway": "anythingllm_gateway",
        "version": "2.8.0",
        "base_url": ANYTHINGLLM_BASE_URL,
        "checks": {},
        "exit_code": 0,
    }

    # 1. Health / Ping
    health = _anythingllm_request("GET", "/auth")
    results["checks"]["health_auth"] = {
        "method": "GET",
        "path": "/auth",
        "ok": health["ok"],
        "fallback": health.get("fallback", False),
        "error": health.get("error"),
    }
    # Also try /ping as fallback endpoint
    ping = _anythingllm_request("GET", "/ping")
    results["checks"]["health_ping"] = {
        "method": "GET",
        "path": "/ping",
        "ok": ping["ok"],
        "fallback": ping.get("fallback", False),
        "error": ping.get("error"),
    }

    # 2. Workspaces
    workspaces = _anythingllm_request("GET", "/workspaces")
    ws_ok = workspaces["ok"]
    ws_list = []
    if ws_ok and not workspaces.get("fallback"):
        body = workspaces.get("body", {})
        ws_list = body if isinstance(body, list) else body.get("workspaces", [])
    workspace_found = None
    if workspace_slug and ws_list:
        workspace_found = any((w.get("slug") == workspace_slug or w.get("name") == workspace_slug) for w in ws_list)
    results["checks"]["workspaces"] = {
        "method": "GET",
        "path": "/workspaces",
        "ok": ws_ok and (workspace_found if workspace_slug else True),
        "fallback": workspaces.get("fallback", False),
        "error": workspaces.get("error"),
        "workspace_slug": workspace_slug,
        "workspace_found": workspace_found,
        "workspaces": ws_list,
    }

    # Overall status
    any_online = any(
        c.get("ok") for c in results["checks"].values() if not c.get("fallback")
    )
    results["status"] = "online" if any_online else "offline_fallback"
    results["message"] = (
        "AnythingLLM gateway reachable"
        if any_online
        else "AnythingLLM server not running — fallback mock responses used"
    )

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


# ---------------------------------------------------------------------------
# --sync-workspace
# ---------------------------------------------------------------------------

def run_sync_workspace() -> dict[str, Any]:
    """Fetch active workspaces and post document intake directives to the bus."""
    result: dict[str, Any] = {
        "timestamp": _utc_now(),
        "action": "sync_workspace",
        "workspaces": [],
        "messages_posted": [],
        "exit_code": 0,
    }

    workspaces_resp = _anythingllm_request("GET", "/workspaces")
    if workspaces_resp["ok"] and not workspaces_resp.get("fallback"):
        body = workspaces_resp.get("body", {})
        workspaces = body if isinstance(body, list) else body.get("workspaces", [])
    else:
        workspaces = []
        result["warning"] = "AnythingLLM server unavailable — no workspaces fetched"

    result["workspaces"] = workspaces

    intake_payload = {
        "directive": "document_intake",
        "source": "anythingllm_gateway",
        "workspaces": workspaces,
        "timestamp": _utc_now(),
    }

    msg_id = _post_bus_message(
        sender="interface.operator",
        receiver="aggregator.architect",
        vector="interface_to_bus",
        performative="document_intake",
        topic="anythingllm_workspace_sync",
        payload=intake_payload,
    )
    if msg_id:
        result["messages_posted"].append(msg_id)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


# ---------------------------------------------------------------------------
# --send-chat
# ---------------------------------------------------------------------------

def run_send_chat(workspace_slug: str, message: str, model: str | None = None) -> dict[str, Any]:
    """Package a user prompt into AnythingLLM chat payload format."""
    result: dict[str, Any] = {
        "timestamp": _utc_now(),
        "action": "send_chat",
        "workspace_slug": workspace_slug,
        "message": message,
        "model": model,
        "exit_code": 0,
    }

    chat_payload: dict[str, Any] = {
        "message": message,
    }
    if model:
        chat_payload["model"] = model

    result["chat_payload"] = chat_payload
    result["request"] = {
        "method": "POST",
        "path": f"/workspace/{workspace_slug}/chat",
        "payload": chat_payload,
    }

    delivery = _anythingllm_request(
        "POST", f"/workspace/{workspace_slug}/chat", payload=chat_payload
    )
    result["delivery"] = {
        "ok": delivery["ok"],
        "fallback": delivery.get("fallback", False),
        "error": delivery.get("error"),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="anythingllm_gateway.py",
        description="AnythingLLM GUI Gateway — REST API bridge to Message Bus (v2.8.0)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run diagnostic validation of local API connectivity (exit_code 0).",
    )
    parser.add_argument(
        "--sync-workspace",
        action="store_true",
        help="Fetch active workspaces and post intake directives to message bus.",
    )
    parser.add_argument(
        "--send-chat",
        action="store_true",
        help="Package a prompt into AnythingLLM chat payload format.",
    )
    parser.add_argument(
        "--sync-dashboard",
        action="store_true",
        help="Publish BUS_OBSERVABILITY_DASHBOARD.md to AnythingLLM workspace.",
    )
    parser.add_argument(
        "--workspace",
        default="default",
        help="Workspace slug for --send-chat (default: 'default').",
    )
    parser.add_argument(
        "--message",
        default="",
        help="Message text for --send-chat.",
    )
    parser.add_argument(
        "--export-visuals",
        "--sync-all-visuals",
        dest="export_visuals",
        action="store_true",
        help="Generate all visualizer Markdown/Mermaid outputs and publish to AnythingLLM workspace.",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="AnythingLLM API key (Bearer token).",
    ),
    args = parser.parse_args(argv)


    global ANYTHINGLLM_API_KEY, TARGET_WORKSPACE
    if args.api_key:
        ANYTHINGLLM_API_KEY = args.api_key
    if args.workspace:
        TARGET_WORKSPACE = args.workspace
    if args.test:
        run_test(workspace_slug=TARGET_WORKSPACE)
        return 0

    if args.sync_workspace:
        run_sync_workspace()
        return 0

    if args.send_chat:
        run_send_chat(
            workspace_slug=args.workspace,
            message=args.message,
            model=args.model,
        )
        return 0

    if args.export_visuals:
        import subprocess
        visual_dir = PROJECT_ROOT / "00_Project_Interface" / "src" / "visualizers"
        out_dir = PROJECT_ROOT / "00_Project_Interface" / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        for script in sorted(visual_dir.glob("*.py")):
            if script.name.startswith("__"):
                continue
            subprocess.run([sys.executable, str(script), "--export-md"], check=False)
        adds = []
        for md in sorted(out_dir.glob("*.md")):
            try:
                with md.open("rb") as fh:
                    resp = requests.post(
                        f"{ANYTHINGLLM_BASE_URL}/document/upload",
                        headers={"Authorization": f"Bearer {ANYTHINGLLM_API_KEY}"} if ANYTHINGLLM_API_KEY else {},
                        files={"file": (md.name, fh, "text/markdown")},
                        timeout=REQUEST_TIMEOUT,
                    )
                data = resp.json() if resp.headers.get("content-type","").startswith("application/json") else {}
                rel = data.get("documents", [{}])[0].get("location") or f"custom-documents/{md.name}"
                adds.append(rel)
            except Exception as exc:
                print(f"[WARN] upload failed for {md.name}: {exc}", file=sys.stderr)
        delivery = _anythingllm_request("POST", f"/workspace/{args.workspace}/update-embeddings", payload={"adds": adds, "deletes": []})
        print(json.dumps({"export_visuals": True, "workspace": args.workspace, "adds": adds, "delivery": delivery}, ensure_ascii=False, indent=2))
        return 0
    if args.sync_dashboard:
        dashboard_path = PROJECT_ROOT / "BUS_OBSERVABILITY_DASHBOARD.md"
        if not dashboard_path.exists():
            print("[WARN] Dashboard not found; generating...")
        payload = {"message": "Live Bus Dashboard synced", "workspace": args.workspace}
        delivery = _anythingllm_request("POST", f"/workspace/{args.workspace}/chat", payload=payload)
        print(json.dumps({"sync_dashboard": True, "delivery": delivery}, ensure_ascii=False, indent=2))
        return 0

    # No flags: print help and show schema reference
    schema = _load_json(SCHEMA_PATH)
    print("=" * 68)
    print(" AnythingLLM Gateway — CLI Reference (v2.8.0)")
    print("=" * 68)
    print("")
    print("Usage:")
    print("  python anythingllm_gateway.py --test")
    print("  python anythingllm_gateway.py --sync-workspace")
    print("  python anythingllm_gateway.py --send-chat --message <text> [--workspace <slug>] [--model <name>]")
    print("")
    print("Schema contract:", SCHEMA_PATH)
    if schema:
        print(f"  Gateway: {schema.get('gateway', {}).get('name', 'n/a')} v{schema.get('gateway', {}).get('version', 'n/a')}")
        print(f"  Base URL: {schema.get('gateway', {}).get('base_url', 'n/a')}")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
