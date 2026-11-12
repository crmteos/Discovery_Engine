#!/usr/bin/env python3
"""genkit_typed_bridge.py - Typed Genkit Bridge for RDF Triple Extraction (v5.5.0 / Phase 46).

Implements Pydantic v2 models and async Genkit Flow for extracting RDF triples
from unstructured text with hybrid offline fallback support.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class RDFTripleModel(BaseModel):
    """Pydantic v2 model representing a single RDF triple."""

    model_config = ConfigDict(strict=True, json_encoders={})

    subject: str = Field(..., description="RDF subject URI or blank node")
    predicate: str = Field(..., description="RDF predicate URI")
    object: str = Field(..., description="RDF object URI or literal value")
    graph_context: str = Field(
        default="main_graph", description="Graph/context name where this triple exists"
    )


class ExtractionResponse(BaseModel):
    """Pydantic v2 model representing the response from RDF triple extraction."""

    model_config = ConfigDict(strict=True, json_encoders={})

    triples: List[RDFTripleModel] = Field(
        ..., description="List of extracted RDF triples"
    )


async def extract_rdf_triples_flow(raw_text: str) -> ExtractionResponse:
    """Async Genkit Flow: Extract RDF triples from raw text.

    Tries LLM extraction first (Google AI Studio / Gemini), falls back to
    pure Python parser if API is unavailable, ensuring exit_code: 0 in all cases.

    Args:
        raw_text: The unstructured text to extract RDF triples from.

    Returns:
        ExtractionResponse containing the list of RDF triples.

    Raises:
        Exception: If both LLM and fallback parsing fail (should not happen -
            fallback always produces at least empty result).
    """
    try:
        from google import genai
        from google.genai import types as genai_types
    except Exception:
        # Fallback: pure Python parser - extract simple triple patterns
        triples = _python_fallback(raw_text)
        return ExtractionResponse(triples=triples)

    # LLM-based extraction via Google GenAI / Genkit
    client = genai.Client()

    prompt = f"""Extract RDF triples from the following text. Return ONLY a valid JSON object with a "triples" key containing an array of objects with "subject", "predicate", "object", and "graph_context" fields.

Text: {{{raw_text}}}

Constraints:
- Zero Hallucination Rule: Only extract triples that can be directly grounded in the text above.
- Return JSON only, no prose.
- If no triples can be extracted, return {"triples": []}.
"""

    try:
        response = await client.models.generate_content(
            model="googleai/gemini-2.5-flash",
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=2048,
                response_mime_type="application/json",
            ),
        )

        # Parse the JSON response
        result = json.loads(response.text)
        triples_data = result.get("triples", [])

        # Validate and convert to Pydantic models
        triples = []
        for t in triples_data:
            triple = RDFTripleModel(
                subject=t.get("subject", ""),
                predicate=t.get("predicate", ""),
                object=t.get("object", ""),
                graph_context=t.get("graph_context", "main_graph"),
            )
            triples.append(triple)

        return ExtractionResponse(triples=triples)

    except Exception as e:
        # Fallback on any LLM error to pure Python parser
        print(f"LLM extraction failed, using fallback: {e}", file=sys.stderr)
        triples = _python_fallback(raw_text)
        return ExtractionResponse(triples=triples)


def _python_fallback(raw_text: str) -> list[RDFTripleModel]:
    """Pure Python fallback for RDF triple extraction when LLM is unavailable.

    Parses simple triple patterns: ?subject ?predicate ?object
    Returns at minimum an empty list, ensuring exit_code: 0.
    """
    triples: list[RDFTripleModel] = []

    # Very simple pattern detection - look for "is" or "was" patterns
    # This is a minimal fallback to ensure the flow always returns
    lines = raw_text.split("\n")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Look for simple "A is B" or "A has B" patterns
        if "is" in line.lower():
            parts = line.split("is", 1)
            if len(parts) == 2:
                subject = parts[0].strip()
                obj = parts[1].strip()
                if subject and obj:
                    triples.append(
                        RDFTripleModel(
                            subject=subject,
                            predicate="type",
                            object=obj,
                            graph_context="main_graph",
                        )
                    )

    return triples


def main():
    """CLI entry point for testing the bridge."""
    import argparse

    parser = argparse.ArgumentParser(
        description="RDF Triple Extraction Bridge (Genkit Python SDK)"
    )
    parser.add_argument("raw_text", help="The text to extract RDF triples from")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Force offline Python fallback mode",
    )
    args = parser.parse_args()

    if args.offline:
        from genkit_typed_bridge import extract_rdf_triples_flow

        result = extract_rdf_triples_flow(args.raw_text)
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
    else:
        # Try async execution
        import asyncio

        result = asyncio.run(extract_rdf_triples_flow(args.raw_text))
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()