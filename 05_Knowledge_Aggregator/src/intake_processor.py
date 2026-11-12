#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""05_Knowledge_Aggregator/src/intake_processor.py — Knowledge Aggregator Intake Processor (v4.7.0 / Phase 38).

Node 05 pipeline: NARROW_EXTRACTOR ➔ ZERO_HALLUCINATION_AUDITOR ➔ KNOWLEDGE_WEAVER
This module performs objective, un-distorted fact extraction from source text.
Axiomatic transformations (basis transformations, Fourier DFT, formal ontology projection)
represent Formal Modeling Operators under ISO/IEC/IEEE 42010, which belong in Node 06
(Formalized Model) and Node 01 (Formal Core). This module is strictly limited to
the 3-stage factual extraction pipeline.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

_INTERFACE_SRC = PROJECT_ROOT.parent / "00_Project_Interface" / "src"
if str(_INTERFACE_SRC) not in sys.path:
    sys.path.insert(0, str(_INTERFACE_SRC))

from google_ai_gateway import _generate_content, _client_for_model, _list_models, GEMINI_API_KEY, GEMINI_MODEL_CHAIN  # type: ignore[import]
from ollama_gateway import _ollama_request, OLLAMA_BASE_URL, REQUEST_TIMEOUT, MODEL_FALLBACK_CHAIN, resolve_model, generate  # type: ignore[import]

logger = logging.getLogger("intake_processor")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s"))