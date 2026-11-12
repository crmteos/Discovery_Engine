#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""05_Knowledge_Aggregator/src/intake_processor.py — Knowledge Aggregator Intake Processor (v4.6.0 / Phase 37)."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

_INTERFACE_SRC = PROJECT_ROOT.parent / "00_Project_Interface" / "src"
if str(_INTERFACE_SRC) not in sys.path:
    sys.path.insert(0, str(_INTERFACE_SRC))

from google_ai_gateway import _generate_content, _client_for_model, _list_models, GEMINI_API_KEY, GEMINI_MODEL_CHAIN  # type: ignore[import]
from ollama_gateway import _ollama_request, OLLAMA_BASE_URL, REQUEST_TIMEOUT, MODEL_FALLBACK_CHAIN, resolve_model, generate  # type: ignore[import]

logger = logging.getLogger("intake_processor")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s"))
def _generate_with_ollama(text: str, model: Optional[str] = None) -> Dict[str, Any]:
    """Extract RDF triple using Ollama gateway.

    Falls back to offline mode if Ollama server is unreachable.
    """
    payload = {
        "model": model or MODEL_FALLBACK_CHAIN[0],
        "prompt": text,
        "stream": False,
    }
    try:
        response = _ollama_request("POST", "/api/generate", payload)
    except Exception as exc:  # broad catch; gateway captures its own errors
        logger.warning(f"Ollama request failed (offline fallback): {exc}")
        return {"subject": "", "predicate": "", "object": "", "graph_context": "offline_fallback"}
    if not response.get("ok", False):
        logger.warning(f"Ollama extraction failed: {response.get('error', 'unknown error')}")
        if response.get("fallback", False):
            return {"subject": "", "predicate": "", "object": "", "graph_context": "offline_fallback"}
        return {"subject": "", "predicate": "", "object": "", "graph_context": "extraction_failed"}
    try:
        generated = response.get("data", {})
        if isinstance(generated, dict):
            content = generated.get("response") or json.dumps(generated)
        else:
            content = str(generated)
        triplet = json.loads(content)
        required_keys = {"subject", "predicate", "object", "graph_context"}
        if not required_keys.issubset(triplet.keys()):
            logger.warning(f"LLM output missing required keys. Got: {triplet}")
            return {"subject": "", "predicate": "", "object": "", "graph_context": "invalid_output"}
        return triplet
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning(f"Failed to parse LLM output as JSON: {exc}")
        return {"subject": "", "predicate": "", "object": "", "graph_context": "parse_error"}


def _generate_with_gemini(text: str, model: Optional[str] = None) -> Dict[str, Any]:
    """Extract RDF triple using Google AI Gateway with Context Caching.

    Falls back to Ollama if GEMINI_API_KEY is missing or API call fails.
    """
    resolved_model = model or GEMINI_MODEL_CHAIN[0]
    client = _client_for_model(resolved_model)
    try:
        result = _generate_content(client, resolved_model, text)
        if result.get("ok", False):
            data = result.get("data", "")
            try:
                triplet = json.loads(data) if data else {}
                required_keys = {"subject", "predicate", "object", "graph_context"}
                if required_keys.issubset(triplet.keys()):
                    return triplet
            except (json.JSONDecodeError, Exception):
                pass
            return {"subject": "", "predicate": "", "object": "", "graph_context": data or "gemini_no_triplet"}
        else:
            logger.info(f"Gemini API failed ({result.get('error')}), falling back to Ollama")
            return _generate_with_ollama(text)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning(f"Gemini generation exception ({exc}), falling back to Ollama")
        return _generate_with_ollama(text)


def extract_triplet(text: str, provider: str = "auto", model: Optional[str] = None) -> Dict[str, Any]:
    """Extract RDF triple from text using the specified provider.

    Args:
        text: Input text to extract triples from.
        provider: One of "auto", "ollama", "google".
        model: Optional model name override.

    Returns:
        Dict with keys: subject, predicate, object, graph_context
    """
    if provider == "auto":
        result = _generate_with_gemini(text, model=model)
        if result.get("graph_context") == "offline_fallback":
            result = _generate_with_ollama(text, model=model)
        return result
    elif provider == "ollama":
        return _generate_with_ollama(text, model=model)
    elif provider == "google":
        return _generate_with_gemini(text, model=model)
    else:
        logger.error(f"Unknown provider: {provider}. Using auto mode.")
        return extract_triplet(text, provider="auto", model=model)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Knowledge Aggregator Intake Processor (v4.6.0 / Phase 37).")
    parser.add_argument(
        "--llm-extract",
        action="store_true",
        help="Run LLM-based RDF triple extraction.",
    )
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        help="Text to process.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model to use (overrides provider default).",
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["auto", "ollama", "google"],
        default="auto",
        help='LLM provider: "auto" tries Gemini then falls back to Ollama, "ollama" uses local Ollama, "google" uses Gemini AI Studio API.',
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (JSON).",
    )
    args = parser.parse_args(argv)

    if not args.llm_extract:
        parser.print_help()
        return 0

    if not args.text:
        parser.print_help()
        print("Error: --text is required for --llm-extract mode.", file=sys.stderr)
        return 1

    logger.info(f"Running --llm-extract mode with provider: {args.provider}")

    triplet = extract_triplet(args.text, provider=args.provider, model=args.model)
    print(json.dumps(triplet, ensure_ascii=False, indent=2))

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(triplet, f, ensure_ascii=False, indent=2)
            logger.info(f"Output written to {args.output}")
        except Exception as exc:
            logger.error(f"Failed to write output to {args.output}: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())