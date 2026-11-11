#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00_Project_Interface/src/ollama_gateway.py — Local Ollama REST Gateway (v3.8.0).

Gateway bridge between the locally-hosted Ollama REST API
(http://127.0.0.1:11434) and the Discovery Engine Message Bus
(Bridge/bus_manager.py).

Supports:
  --test        Diagnostic validation of local Ollama connectivity: liveness
                ping (/api/tags), model fallback-chain resolution
                (qwen2.5-coder:14b -> llama3.1:8b -> qwen2.5:7b), and a
                smoke /api/generate call against the first available model.
                Graceful fallback (offline mode) when the Ollama server is
                not reachable. Structured status with exit_code: 0.
  --resolve     Print the resolved model from the fallback chain.
  --generate    Send a prompt to /api/generate using the resolved model.

Zero external native dependencies: uses only `requests` (already in the stack).
Budget: $0.00 — pure local CPU inference via Ollama. No paid APIs, no cloud.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import requests
except ImportError:  # pragma: no cover - requests is part of the approved stack
    requests = None  # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"

# Ensure Bridge/ is importable for bus_manager telemetry logging.
if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
REQUEST_TIMEOUT = 5
MODEL_FALLBACK_CHAIN: list[str] = ["qwen2.5-coder:14b", "llama3.1:8b", "qwen2.5:7b"]
DEFAULT_MODEL = MODEL_FALLBACK_CHAIN[0]
SMOKE_PROMPT = "2+2="
def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ollama_request(
    method: str,
    path: str,
    payload: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Make a request to the Ollama REST API with graceful offline fallback.

    Never raises: connection errors are captured and returned as
    ``{"ok": False, "fallback": True, ...}`` so callers can degrade
    gracefully when the Ollama server is not running.
    """
    if requests is None:
        return {
            "ok": False,
            "error": "requests package not installed",
            "fallback": True,
            "url": f"{OLLAMA_BASE_URL}{path}",
        }
    url = f"{OLLAMA_BASE_URL}{path}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        else:
            return {"ok": False, "error": f"unsupported method {method}", "fallback": True, "url": url}
        try:
            data = response.json()
        except ValueError:
            data = {"raw_text": response.text[:500]}
        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "data": data,
            "fallback": False,
            "url": url,
        }
    except OSError as exc:  # includes requests.ConnectionError, ConnectTimeout, etc.
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "fallback": True,
            "url": url,
        }


def ping() -> dict[str, Any]:
    """Liveness ping to the local Ollama API (GET /api/tags)."""
    return _ollama_request("GET", "/api/tags")


def list_models() -> list[str]:
    """Return the list of model names available on the local Ollama server."""
    response = ping()
    if not response.get("ok"):
        return []
    data = response.get("data", {}) or {}
    models = data.get("models", []) or []
    names: list[str] = []
    for entry in models:
        if isinstance(entry, dict) and entry.get("name"):
            names.append(entry["name"])
        elif isinstance(entry, str):
            names.append(entry)
    return names


def resolve_model(preferred: Optional[str] = None) -> Optional[str]:
    """Resolve the first available model from the fallback chain.

    Order: qwen2.5-coder:14b -> llama3.1:8b -> qwen2.5:7b.
    Returns None when the server is offline or none of the chain models exist.
    """
    available = set(list_models())
    chain = [preferred] + MODEL_FALLBACK_CHAIN if preferred else list(MODEL_FALLBACK_CHAIN)
    seen: set[str] = set()
    for model in chain:
        if not model or model in seen:
            continue
        seen.add(model)
        if model in available:
            return model
    # Last resort: return the first model the server knows about, else the
    # default chain head so callers can still attempt a generate call.
    if available:
        return sorted(available)[0]
    return DEFAULT_MODEL


def generate(model: str, prompt: str, stream: bool = False) -> dict[str, Any]:
    """Send a completion request to POST /api/generate with graceful fallback."""
    payload = {"model": model, "prompt": prompt, "stream": stream}
    return _ollama_request("POST", "/api/generate", payload=payload)


def _post_bus_telemetry(step_name: str, metrics: dict[str, Any], status: str) -> None:
    """Best-effort telemetry log to Bridge/messages.jsonl via bus_manager."""
    try:
        from bus_manager import log_core_telemetry  # type: ignore

        log_core_telemetry(step_name=step_name, metrics=metrics, status=status)
    except Exception as exc:  # pragma: no cover - telemetry must never crash the gateway
        print(f"[WARN] Could not post telemetry to message bus: {exc}", file=sys.stderr)
def run_test() -> int:
    """Standalone --test mode: ping Ollama, resolve fallback-chain model,
    smoke-generate against the resolved model, print structured status."""
    report: dict[str, Any] = {
        "gateway": "ollama_gateway.py",
        "version": "3.8.0",
        "base_url": OLLAMA_BASE_URL,
        "timestamp_utc": _utc_now(),
        "fallback_chain": list(MODEL_FALLBACK_CHAIN),
        "requests_available": requests is not None,
    }

    # 1. Liveness ping
    ping_response = ping()
    report["ping"] = {
        "ok": ping_response.get("ok", False),
        "status_code": ping_response.get("status_code"),
        "fallback": ping_response.get("fallback", False),
        "error": ping_response.get("error"),
    }

    # 2. Fallback-chain model resolution
    available_models = list_models() if ping_response.get("ok") else []
    report["available_models"] = available_models
    resolved = resolve_model()
    report["resolved_model"] = resolved
    report["resolved_vs_default"] = resolved == DEFAULT_MODEL

    # 3. Smoke /api/generate against resolved model (graceful if offline)
    generate_response: Optional[dict[str, Any]] = None
    if resolved:
        generate_response = generate(resolved, SMOKE_PROMPT)
        report["generate"] = {
            "model": resolved,
            "prompt": SMOKE_PROMPT,
            "ok": generate_response.get("ok", False),
            "status_code": generate_response.get("status_code"),
            "fallback": generate_response.get("fallback", False),
            "error": generate_response.get("error"),
            "response": generate_response.get("data"),
        }
    else:
        report["generate"] = {
            "model": None,
            "skipped": True,
            "reason": "no model resolved (server offline or chain models missing)",
        }

    # 4. Telemetry to the message bus (best effort)
    all_ok = bool(ping_response.get("ok")) and resolved is not None
    telemetry_status = "completed" if all_ok else "degraded_offline"
    _post_bus_telemetry(
        step_name="ollama_gateway_test",
        metrics={
            "ping_ok": ping_response.get("ok", False),
            "resolved_model": resolved,
            "available_models": available_models,
            "generate_ok": generate_response.get("ok") if generate_response else None,
        },
        status=telemetry_status,
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("-" * 68)
    print(f"Ollama gateway --test: {telemetry_status.upper()}")
    print(f"  Ping /api/tags: {'OK' if ping_response.get('ok') else 'OFFLINE/FALLBACK'}")
    print(f"  Fallback chain: {' -> '.join(MODEL_FALLBACK_CHAIN)}")
    print(f"  Resolved model: {resolved or 'none (offline fallback)'}")
    print("  Budget: $0.00 | Local CPU via Ollama")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Local Ollama REST Gateway (v3.8.0) — discovery-engine local LLM binding."
    )
    parser.add_argument("--test", action="store_true", help="Run diagnostic validation (ping + fallback resolve + smoke generate).")
    parser.add_argument("--resolve", action="store_true", help="Print the resolved fallback-chain model name and exit.")
    parser.add_argument("--model", default=None, help="Model to use for --generate (defaults to resolved fallback model).")
    parser.add_argument("--prompt", default=SMOKE_PROMPT, help="Prompt for --generate.")
    args = parser.parse_args(argv)

    if args.test:
        return run_test()

    if args.resolve:
        resolved = resolve_model()
        print(json.dumps({"resolved_model": resolved, "fallback_chain": MODEL_FALLBACK_CHAIN}, ensure_ascii=False))
        return 0

    if args.prompt or args.model != SMOKE_PROMPT:
        model = args.model or resolve_model() or DEFAULT_MODEL
        response = generate(model, args.prompt)
        print(json.dumps({"model": model, "prompt": args.prompt, "delivery": response}, ensure_ascii=False, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
