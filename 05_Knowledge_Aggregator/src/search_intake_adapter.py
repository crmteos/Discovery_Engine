#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""05_Knowledge_Aggregator/src/search_intake_adapter.py — OSINT Search & AI Grounding Intake Adapter (v4.3.0 / Phase 34)"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BRIDGE_DIR = PROJECT_ROOT / "Bridge"
if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

INTERFACE_SRC = PROJECT_ROOT.parent / "00_Project_Interface" / "src"
if str(INTERFACE_SRC) not in sys.path:
    sys.path.insert(0, str(INTERFACE_SRC))

from ollama_gateway import _ollama_request, OLLAMA_BASE_URL, REQUEST_TIMEOUT  # type: ignore[import]

INTAKE_PROCESSOR = PROJECT_ROOT / "05_Knowledge_Aggregator" / "src" / "intake_processor.py"
if str(INTAKE_PROCESSOR.parent) not in sys.path:
    sys.path.insert(0, str(INTAKE_PROCESSOR.parent))

from intake_processor import extract_triplet_with_llm  # type: ignore[import]

def search_duckduckgo(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """Perform zero-cost search using DuckDuckGo HTML API."""
    try:
        import requests
        params = {"q": query, "kl": "us-en"}
        response = requests.get(DUCKDUCKGO_BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            logger.warning(f"DuckDuckGo returned status {response.status_code}")
            return []
        import re
        html = response.text
        title_pattern = r'class="result__title[^"]*"[^>]*>([^<]+)</a>'
        title_matches = re.findall(title_pattern, html)
        snippet_pattern = r'class="result__snippet[^"]*"[^>]*>([^<]+)</a>'
        snippet_matches = re.findall(snippet_pattern, html)
        url_pattern = r'class="result__a[^"]*"[^>]*href="([^"]+)"'
        url_matches = re.findall(url_pattern, html)
        results = []
        for i in range(min(len(title_matches), len(url_matches), max_results)):
            title = title_matches[i].strip() if i < len(title_matches) else ""
            url = url_matches[i] if i < len(url_matches) else ""
            snippet = snippet_matches[i] if i < len(snippet_matches) else ""
            title = re.sub(r"<[^>]+>", "", title).strip()
            url = url.replace('"', '"').replace('&', '&')
            if title and url:
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet.strip() if i < len(snippet_matches) else "",
                    "source": "duckduckgo",
                })
        logger.info(f"DuckDuckGo search '{query}' returned {len(results)} results")
        return results
    except ImportError:
        logger.warning("requests package not available")
        return []
    except Exception as exc:
        logger.warning(f"Search request failed (offline fallback): {exc}")
        return []


def generate_intake_draft(query: str, results: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
    """Generate structured JSON intake draft from search results."""
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    draft = {
        "query": query,
        "results": results,
        "generated_at": generated_at,
        "metadata": {
            "provider": "duckduckgo",
            "search_time_ms": int(time.time() * 1000) % 10000,
            "result_count": len(results),
        },
    }
    if model and results:
        try:
            text_parts = []
            for r in results[:3]:
                text_parts.append(f"Title: {r.get('title', '')}")
                text_parts.append(f"Snippet: {r.get('snippet', '')}")
            combined_text = "\n".join(text_parts)
            triplet = extract_triplet_with_llm(combined_text, model=model)
            if triplet and triplet.get("subject"):
                draft["extracted_triplet"] = triplet
                draft["metadata"]["triplet_extracted"] = True
            else:
                draft["metadata"]["triplet_extracted"] = False
        except Exception as exc:
            logger.warning(f"LLM triplet extraction failed: {exc}")
            draft["metadata"]["triplet_extracted"] = False
    else:
        draft["metadata"]["triplet_extracted"] = False
    if results:
        draft["metadata"]["prov:wasDerivedFrom"] = results[0].get("url", "")
        draft["metadata"]["skos:Concept"] = {
            "prefLabel": query,
            "altLabels": [query],
            "definition": f"OSINT search results for query: {query}",
        }
    return draft


def write_draft_to_disk(draft: Dict[str, Any], filename: Optional[str] = None) -> Path:
    """Write intake draft to disk as JSON in Intake_Queue/drafts/."""
    if filename is None:
        import hashlib
        query = draft.get("query", "unknown")
        safe_query = "".join(c if c.isalnum() or c in "-" "_" else "_" for c in query)[:50]
        filename = f"draft_{safe_query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    draft_path = INTAKE_QUEUE_DRAFTS_DIR / filename
    try:
        with open(draft_path, "w", encoding="utf-8") as f:
            json.dump(draft, f, ensure_ascii=False, indent=2)
        logger.info(f"Intake draft written to {draft_path}")
        return draft_path
    except Exception as exc:
        logger.error(f"Failed to write intake draft: {exc}")
        raise


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="OSINT Search & AI Grounding Intake Adapter (v4.3.0 / Phase 34).")
    parser.add_argument("--query", type=str, default=None, help="Search query to process")
    parser.add_argument("--output", type=str, default=None, help="Output file path (JSON)")
    parser.add_argument("--model", type=str, default=None, help="Ollama model for triplet extraction")
    parser.add_argument("--offline", action="store_true", help="Run in offline mode")
    args = parser.parse_args(argv)

    query: str = args.query or "Discovery Engine knowledge graph cognitive models"

    if args.offline:
        logger.info("Running in offline mode: loading existing drafts.")
        drafts_dir = INTAKE_QUEUE_DRAFTS_DIR
        if drafts_dir.exists() and any(drafts_dir.iterdir()):
            for draft_file in sorted(drafts_dir.glob("*.json")):
                try:
                    with open(draft_file, "r", encoding="utf-8") as f:
                        draft = json.load(f)
                    print(json.dumps(draft, ensure_ascii=False, indent=2))
                    print("-" * 60)
                except Exception as exc:
                    logger.warning(f"Failed to load draft {draft_file}: {exc}")
        else:
            logger.info("No existing drafts found in offline mode.")
        return 0

    logger.info(f"Running search intake adapter with query: {query}")
    results = search_duckduckgo(query)

    if not results:
        logger.warning("No search results returned - proceeding with empty draft")

    draft = generate_intake_draft(query, results, model=args.model)

    output_json = json.dumps(draft, ensure_ascii=False, indent=2)
    print(output_json)

    output_path = args.output
    if not output_path:
        output_path = str(
            write_draft_to_disk(draft, filename=f"draft_{query.replace(' ', '_')}.json")
        )

    if output_path and not os.path.isabs(output_path):
        output_path = str(PROJECT_ROOT / output_path)

    if output_path:
        try:
            final_path = write_draft_to_disk(draft, filename=output_path)
            print(f"\nDraft written to: {final_path}")
        except Exception as exc:
            logger.error(f"Failed to write draft to disk: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())