#!/usr/bin/env python3
"""Integration test for Phase 34: OSINT Search & AI Grounding Intake Adapter.

Tests the search_intake_adapter.py end-to-end pipeline:
- py_compile verification
- Query-based search and draft creation
- Graceful offline fallback mode
- JSON schema validation of generated drafts
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Add project roots to path - following pattern, but pointing to src/ directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "05_Knowledge_Aggregator" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "00_Project_Interface" / "src" / "ollama_gateway.py" if False else "00_Project_Interface/src"))

from search_intake_adapter import (
    generate_intake_draft,
    search_duckduckgo,
    write_draft_to_disk,
)