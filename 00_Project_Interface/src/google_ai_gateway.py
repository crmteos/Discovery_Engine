#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00_Project_Interface/src/google_ai_gateway.py — Google AI Gateway (v5.3.0 / Phase 44).
Google AI Gateway with Enterprise Switcher & Data Residency (EU/US) support.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import google.genai as genai  # type: ignore[import]
    from google.genai import types  # type: ignore[import]
except ImportError:  # pragma: no cover
    genai = None  # type: ignore[assignment]
    types = None  # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"

if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
VERTEX_AI_ENABLED = os.environ.get("VERTEX_AI_ENABLED", "").lower() in ("true", "1")
VERTEX_LOCATION = os.environ.get("VERTEX_LOCATION", "europe-west1")
GCPGCP_PROJECT_ID = os.environ.get("GCPGCP_PROJECT_ID", "")

GEMINI_MODEL_CHAIN: list[str] = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]
DEFAULT_MODEL = GEMINI_MODEL_CHAIN[0]

# Context Caching configuration (v4.5.0 / Phase 36)
CACHE_TTL_SECONDS = 300  # 5 minutes default TTL for specification caches
CACHE_DIR_NAME = ".cache"
SPEC_CACHE_TTL = 300  # 5 minutes for PROJECT_SPEC.md
CONTEXT_CACHE_TTL = 600  # 10 minutes for PROJECT_CONTEXT.md

SMOKE_PROMPT = "2+2="
def _client_for_model(model_name: str, enterprise: bool = False, location: str = "europe-west1", project_id: str = "") -> Any:
    """Create a google-genai client configured for the given model name.

    Args:
        model_name: model to use (e.g. "gemini-2.5-flash")
        enterprise: if True, use Vertex AI authentication
        location: data residency location (europe-west1 or us-central1)
        project_id: GCP project ID for Vertex AI

    Returns:
        google-genai client or None
    """
    if genai is None:
        return None
    try:
        if enterprise and project_id:
            client = genai.Client(vertexai=True, project=project_id, location=location)
        elif enterprise and not project_id:
            # Enterprise mode requested but no project ID - fallback to studio
            client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            client = genai.Client(api_key=GEMINI_API_KEY)
        return client
    except Exception:
        return None


def _generate_content(client, model_name: str, prompt: str, cached_content_config: Any = None, enterprise: bool = False, location: str = "europe-west1", project_id: str = "") -> dict[str, Any]:
    """Generate content using google-genai SDK.

    Args:
        client: google-genai client
        model_name: model to use (e.g. "gemini-2.5-flash")
        prompt: prompt text
        cached_content_config: optional GenerateContentConfig with cached_content reference
        enterprise: whether enterprise mode is enabled
        location: data residency location
        project_id: GCP project ID

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
        generate_config: Any = {}
        if cached_content_config is not None:
            generate_config["cached_content"] = cached_content_config

        # Use vertexai parameters if enterprise mode
        if enterprise and project_id:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                **generate_config,
                vertexai=True,
                project=project_id,
                location=location,
            )
        else:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                **generate_config,
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


def _cache_dir() -> Path:
    """Return the path to the local cache directory."""
    p = PROJECT_ROOT / CACHE_DIR_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def _cache_path(suffix: str) -> Path:
    """Return the path for a cache file with the given suffix."""
    return _cache_dir() / f"gemini_cache{suffix}.json"


def _load_cached_content(suffix: str) -> Optional[dict[str, Any]]:
    """Load cached content from local cache file if it exists and is fresh."""
    cp = _cache_path(suffix)
    if not cp.is_file():
        return None
    try:
        import json
        mtime = cp.stat().st_mtime
        age = datetime.now().timestamp() - mtime
        ttl = {
            "spec": SPEC_CACHE_TTL,
            "context": CONTEXT_CACHE_TTL,
        }.get(suffix, CACHE_TTL_SECONDS)
        if age > ttl:
            # Stale cache, remove and re-create
            cp.unlink(missing_ok=True)
            return None
        with open(cp, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"ok": True, "data": data, "cached": True, "age_seconds": int(age)}
    except Exception:
        # Corrupt cache, remove and re-create
        cp.unlink(missing_ok=True)
        return None


def _save_cached_content(suffix: str, content: str) -> dict[str, Any]:
    """Save specification/content to local cache file."""
    cp = _cache_path(suffix)
    try:
        import json
        with open(cp, "w", encoding="utf-8") as f:
            json.dump({"saved_at": _utc_now(), "content": content}, f, ensure_ascii=False)
        return {"ok": True, "cached": False, "path": str(cp)}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}", "cached": False}


def _google_cache_create(client, model: str, system_instruction: str, ttl: int) -> dict[str, Any]:
    """Create a Gemini Context Cache via google-genai SDK.

    Returns dict with keys: ok, cache_name, cached_content_ref, error, fallback.
    """
    if genai is None or types is None or client is None:
        return {"ok": False, "fallback": True, "error": "google-genai SDK not available"}
    try:
        cache = client.caches.create(
            model=model,
            system_instruction=types.Part(text=system_instruction),
            ttl=ttl,
        )
        # The cached_content reference format for generate_content config
        cached_content_ref = types.GenerateContentConfig(cached_content=cache.name)
        return {"ok": True, "cache_name": cache.name, "cached_content_ref": cached_content_ref, "fallback": False}
    except Exception as exc:  # pylint: disable=broad-except
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}", "fallback": True}


def _google_cache_get(client, model: str, ttl: int) -> dict[str, Any]:
    """Try to get existing cache or create new one.

    Returns dict with keys: ok, cache_name, cached_content_ref, error, fallback.
    """
    if genai is None or types is None or client is None:
        return {"ok": False, "fallback": True, "error": "google-genai SDK not available"}
    try:
        # List existing caches for this model
        caches = client.caches.list()
        # Find a cache that matches our needs (simplified: use first valid cache)
        cache_name = None
        for c in caches:
            # In a real implementation, we'd match by system_instruction hash
            cache_name = c.name
            break
        if cache_name:
            cached_content_ref = types.GenerateContentConfig(cached_content=cache_name)
            return {"ok": True, "cache_name": cache_name, "cached_content_ref": cached_content_ref, "fallback": False}
        # No existing cache, create new one
        return _google_cache_create(client, model, "", ttl)
    except Exception as exc:  # pylint: disable=broad-except
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}", "fallback": True}


def _cache_stats(enterprise: bool = False, location: str = "europe-west1", project_id: str = "") -> int:
    """Report active cache metadata and status.

    Args:
        enterprise: whether enterprise mode is enabled
        location: data residency location
        project_id: GCP project ID
    """
    import json as _json

    spec_cache = _load_cached_content("spec")
    context_cache = _load_cached_content("context")

    # Read cache directory size
    cache_dir = _cache_dir()
    total_size = 0
    file_count = 0
    if cache_dir.is_dir():
        for f in cache_dir.iterdir():
            if f.is_file():
                total_size += f.stat().st_size
                file_count += 1

    report: dict[str, Any] = {
        "cache_dir": str(cache_dir),
        "total_size_bytes": total_size,
        "file_count": file_count,
        "spec_cache": {
            "suffix": "spec",
            "exists": spec_cache is not None,
            "age_seconds": spec_cache.get("age_seconds") if spec_cache else None,
            "cached": spec_cache.get("cached") if spec_cache else False,
        },
        "context_cache": {
            "suffix": "context",
            "exists": context_cache is not None,
            "age_seconds": context_cache.get("age_seconds") if context_cache else None,
            "cached": context_cache.get("cached") if context_cache else False,
        },
        "ttl_config": {
            "spec_ttl_seconds": SPEC_CACHE_TTL,
            "context_ttl_seconds": CONTEXT_CACHE_TTL,
            "default_ttl_seconds": CACHE_TTL_SECONDS,
        },
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("-" * 52)
    print(f"Google AI Gateway Context Caching Stats (v5.3.0 / Phase 44)")
    print(f"Enterprise: {enterprise}, Location: {location}")
    if project_id:
        print(f"GCP Project ID: {project_id}")
    print("-" * 52)
    return 0


def run_test(enterprise: bool = False, location: str = "europe-west1") -> int:
    """Run diagnostic validation test.

    Args:
        enterprise: whether enterprise mode is enabled
        location: data residency location

    Returns:
        exit code (always 0 for graceful fallback)
    """
    print("=== Google AI Gateway Test (v5.3.0 / Phase 44) ===")
    print(f"Enterprise mode: {enterprise}")
    print(f"Location: {location}")
    print()

    # Initialize client based on enterprise flag
    client = _client_for_model(DEFAULT_MODEL, enterprise=enterprise, location=location, project_id=GCPGCP_PROJECT_ID)

    # Determine resolved model
    resolved_model = None
    available_models: list[str] = []

    if client is not None:
        available_models = _list_models(client, enterprise=enterprise, location=location, project_id=GCPGCP_PROJECT_ID)
        print(f"Available models: {available_models}")

    # Try model chain resolution
    for model_name in GEMINI_MODEL_CHAIN:
        if model_name in available_models:
            resolved_model = model_name
            break

    # If no model resolved in enterprise mode, try fallback chain
    if not resolved_model and not enterprise:
        for model_name in GEMINI_MODEL_CHAIN:
            if model_name in available_models:
                resolved_model = model_name
                break

    # Generate smoke prompt
    generation_result = None
    if resolved_model and client is not None:
        generation_result = _generate_content(
            client, resolved_model, SMOKE_PROMPT,
            enterprise=enterprise, location=location, project_id=GCPGCP_PROJECT_ID,
        )
    else:
        generation_result = _generate_content(
            client, DEFAULT_MODEL, SMOKE_PROMPT,
            enterprise=enterprise, location=location, project_id=GCPGCP_PROJECT_ID,
        )

    # Build report
    report = {
        "timestamp": _utc_now(),
        "enterprise": enterprise,
        "location": location,
        "resolved_model": resolved_model,
        "available_models": available_models,
        "generation_ok": generation_result.get("ok", False) if generation_result else False,
        "generation_error": generation_result.get("error") if generation_result else None,
        "fallback": generation_result.get("fallback", True) if generation_result else True,
        "status_code": generation_result.get("status_code", 0) if generation_result else 0,
    }

    # Ping status
    report["ping_ok"] = generation_result is not None and generation_result.get("ok", False) if generation_result else False

    # Telemetry status
    all_ok = bool(GEMINI_API_KEY) and resolved_model is not None
    telemetry_status = "completed" if all_ok else "degraded_offline"
    report["telemetry_status"] = telemetry_status

    # Post telemetry to the message bus (best effort)
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

    # Print report
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("-" * 68)
    print(f"Google AI gateway --test: {telemetry_status.upper()}")
    print(f"  Ping/API available: {'OK' if report['ping_ok'] else 'OFFLINE/FALLBACK'}")
    print(f"  Resolved model: {resolved_model or 'none (offline fallback)'}")
    print(f"  Enterprise: {enterprise}, Location: {location}")
    print(f"  Budget: $0.00 | Google AI Studio free tier + Local Ollama fallback")
    print("-" * 34)

    # Always return exit_code: 0 (graceful fallback even on failure)
    return 0

    if args.cache_stats:
        _cache_stats(enterprise=enterprise, location=location, project_id=GCPGCP_PROJECT_ID)
        return 0

    parser.print_help()
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Google AI Gateway (v5.3.0) — discovery-engine Google AI binding with Context Caching and Enterprise Switcher.",
    )
    parser.add_argument(
        "--enterprise",
        action="store_true",
        help="Enable Vertex AI mode (Enterprise). Switches SDK to Vertex AI authentication via GCP project ID and location.",
    )
    parser.add_argument(
        "--location",
        type=str,
        default="europe-west1",
        help="Data residency location (eu: europe-west1, us: us-central1). Default: europe-west1",
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
    parser.add_argument(
        "--cache-stats",
        action="store_true",
        help="Report active cache metadata and status (spec/context TTL, file sizes).",
    )
    args = parser.parse_args(argv)

    enterprise = args.enterprise
    location = args.location

    # Validate location
    if location not in ("europe-west1", "us-central1"):
        print(f"Warning: Unknown location '{location}'. Using default 'europe-west1'.")
        location = "europe-west1"

    if args.test:
        return run_test(enterprise=enterprise, location=location)

    if args.resolve:
        if genai is not None and GEMINI_API_KEY:
            client = _client_for_model(DEFAULT_MODEL, enterprise=enterprise, location=location, project_id=GCP_PROJECT_ID)
            available = _list_models(client, enterprise=enterprise, location=location, project_id=GCP_PROJECT_ID) if client else []
            resolved = None
            for model_name in GEMINI_MODEL_CHAIN:
                if model_name in available:
                    resolved = model_name
                    break
            print(json.dumps({"resolved_model": resolved, "model_chain": GEMINI_MODEL_CHAIN, "enterprise": enterprise, "location": location}, ensure_ascii=False))
        else:
            print(json.dumps({"resolved_model": None, "model_chain": GEMINI_MODEL_CHAIN, "enterprise": enterprise, "location": location, "gemini_api_key_present": bool(GEMINI_API_KEY)}))
        return 0

    if args.cache_stats:
        _cache_stats(enterprise=enterprise, location=location, project_id=GCP_PROJECT_ID)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
