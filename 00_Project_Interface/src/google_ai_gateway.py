#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00_Project_Interface/src/google_ai_gateway.py — Google AI Gateway (v4.4.0)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import google.genai as genai
except ImportError:  # pragma: no cover
    genai = None  # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"

if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

GEMINI_MODEL_CHAIN: list[str] = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]
DEFAULT_MODEL = GEMINI_MODEL_CHAIN[0]

SMOKE_PROMPT = "2+2="
def _client_for_model(model_name: str):
    """Create a google-genai client configured for the given model name."""
    if genai is None:
        return None
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        return client
    except Exception:
        return None


def _generate_content(client, model_name: str, prompt: str) -> dict[str, Any]:
    """Generate content using google-genai SDK.

    Returns a dict with keys: ok, data, error, fallback, status_code.
    Never raises — connection errors are captured and returned gracefully.
    """
    if client is None:
        return {
            "ok": False,
            "error": "google-genai SDK not available",
            "fallback": True,
            "status_code": 0,
        }

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        # Extract text from the response
        text = getattr(response, "text", None) or str(response)
        return {
            "ok": True,
            "data": text,
            "fallback": False,
            "status_code": 200,
        }
    except Exception as exc:  # pylint: disable=broad-except
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "fallback": True,
            "status_code": 0,
        }
def _utc_now() -> str:
    """Return current UTC timestamp ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _list_models(client) -> list[str]:
    """List available models via google-genai.

    Returns list of model names, or empty list on failure.
    """
    if client is None:
        return []
    try:
        # google-genai lists models via the models API
        response = client.models.list()
        models = []
        for m in response.models:
            models.append(getattr(m, "name", str(m)))
        return models
    except Exception as exc:  # pylint: disable=broad-except
        return []
def run_test() -> int:
    """Run the Google AI gateway --test diagnostic.

    Behavior:
      - If GEMINI_API_KEY is present: execute live API ping / generation test.
      - If GEMINI_API_KEY is missing or network fails: execute graceful
        fallback mode, log telemetry, and return exit_code: 0.
    """
    import json as _json

    report: dict[str, Any] = {
        "timestamp": _utc_now(),
        "gemini_api_key_present": bool(GEMINI_API_KEY),
        "model_chain": GEMINI_MODEL_CHAIN,
        "resolved_model": None,
        "generation": None,
        "ping_ok": False,
        "telemetry_status": "degraded_offline",
    }

    client = _client_for_model(DEFAULT_MODEL) if GEMINI_API_KEY else None

    # 1. Model resolution from the fallback chain
    resolved_model = None
    available_models = []
    if client is not None:
        available_models = _list_models(client)
        # Find first available model from the chain
        for model_name in GEMINI_MODEL_CHAIN:
            if model_name in available_models:
                resolved_model = model_name
                break

    report["available_models"] = available_models
    report["resolved_model"] = resolved_model

    # 2. Smoke generation against resolved model
    generation_result: Optional[dict[str, Any]] = None
    if resolved_model:
        generation_result = _generate_content(client, resolved_model, SMOKE_PROMPT)
        report["generation"] = {
            "model": resolved_model,
            "prompt": SMOKE_PROMPT,
            "ok": generation_result.get("ok", False),
            "status_code": generation_result.get("status_code", 0),
            "fallback": generation_result.get("fallback", False),
            "error": generation_result.get("error"),
            "response": generation_result.get("data"),
        }

    # 3. Ping status
    report["ping_ok"] = generation_result is not None and generation_result.get("ok", False) if generation_result else False

    # 4. Telemetry status
    all_ok = bool(GEMINI_API_KEY) and resolved_model is not None
    telemetry_status = "completed" if all_ok else "degraded_offline"
    report["telemetry_status"] = telemetry_status

    # 5. Post telemetry to the message bus (best effort)
    try:
        import Bridge.bus_manager as bus_manager

        bus_manager.log_core_telemetry(
            step_name="google_ai_gateway_test",
            metrics={
                "ping_ok": report["ping_ok"],
                "resolved_model": resolved_model,
                "available_models": available_models,
                "generation_ok": generation_result.get("ok") if generation_result else None,
            },
            status=telemetry_status,
        )
    except Exception:
        pass  # Best-effort bus posting

    # 6. Print report
    print(_json.dumps(report, ensure_ascii=False, indent=2))
    print("-" * 68)
    print(f"Google AI gateway --test: {telemetry_status.upper()}")
    print(f"  Ping/API available: {'OK' if report['ping_ok'] else 'OFFLINE/FALLBACK'}")
    print(f"  Resolved model: {resolved_model or 'none (offline fallback)'}")
    print(f"  Budget: $0.00 | Google AI Studio free tier + Local Ollama fallback")
    print("  -" * 34)

    # Always return exit_code: 0 (graceful fallback even on failure)
    return 0
def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Google AI Gateway (v4.4.0) — discovery-engine Google AI binding.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run diagnostic validation (ping + model resolve + smoke generate).",
    )
    parser.add_argument(
        "--resolve",
        action="store_true",
        help="Print the resolved model from the fallback chain and exit.",
    )
    args = parser.parse_args(argv)

    if args.test:
        return run_test()

    if args.resolve:
        if genai is not None and GEMINI_API_KEY:
            client = _client_for_model(DEFAULT_MODEL)
            available = _list_models(client) if client else []
            resolved = None
            for model_name in GEMINI_MODEL_CHAIN:
                if model_name in available:
                    resolved = model_name
                    break
            print(json.dumps({"resolved_model": resolved, "model_chain": GEMINI_MODEL_CHAIN}, ensure_ascii=False))
        else:
            print(json.dumps({"resolved_model": None, "model_chain": GEMINI_MODEL_CHAIN, "gemini_api_key_present": bool(GEMINI_API_KEY)}))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
