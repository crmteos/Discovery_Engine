#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""05_Knowledge_Aggregator/src/intake_processor.py — Knowledge Aggregator Intake Processor (v4.2.0 / Phase 33)"""

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

from ollama_gateway import _ollama_request, OLLAMA_BASE_URL, REQUEST_TIMEOUT  # type: ignore[import]

logger = logging.getLogger("intake_processor")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Knowledge Aggregator Intake Processor (v4.2.0 / Phase 33).")
    parser.add_argument("--llm-extract", action="store_true", help="Run LLM-based RDF triple extraction.")
    parser.add_argument("--text", type=str, default=None, help='Text to process.')
    parser.add_argument("--model", type=str, default=None, help='Ollama model to use.')
    parser.add_argument("--output", type=str, default=None, help="Output file path (JSON).")
    args = parser.parse_args(argv)
    if not args.llm_extract:
        parser.print_help()
        return 0
    text = args.text or "The Discovery Engine project uses a local Ollama server."
    logger.info("Running --llm-extract mode.")
    triplet = extract_triplet_with_llm(text, model=args.model)
    print(json.dumps(triplet, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())


# ---------------------------------------------------------------------------
# LLM Extraction helper
# ---------------------------------------------------------------------------


def extract_triplet_with_llm(text: str, model: Optional[str] = None) -> Dict[str, Any]:
    """Send unstructured text to the Ollama Gateway for RDF triplet extraction."""
    payload = {
        "model": model or "qwen2.5-coder:14b",
        "prompt": text,
        "stream": False,
    }
    try:
        response = _ollama_request("POST", "/api/generate", payload)
    except Exception as exc:  # broad catch; _ollama_request captures its own errors
        logger.warning(f"Ollama request failed (offline fallback): {exc}")
        return {"subject": "", "predicate": "", "object": "", "graph_context": "offline_fallback"}
    if not response.get("ok", False):
        logger.warning(f"LLM extraction failed: {response.get('error', 'unknown error')}")
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