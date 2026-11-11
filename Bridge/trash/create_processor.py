#!/usr/bin/env python3
"""Script to create complete intake_processor.py for Cross-Media RDF Linking"""

import os

os.chdir(r"C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine")

filepath = "05_Knowledge_Aggregator/intake_processor.py"

# Write file in parts to avoid quote issues
part1 = '''"""
Intake Processor: Validates incoming cognitive models and maps them into 01_Formal_Core.

Handles five intake categories:
  - raw_cognitive_models   -> cognitive_model_template.json schema
  - structural_analogies   -> analogy_template.json schema
  - conceptual_schemes     -> concept_scheme_template.json schema
  - image_metadata         -> image_metadata_template.json schema
  - video_index            -> video_index_template.json schema

Each validated draft is normalized into a status envelope and written to
Processed_Gate/normalized_triples/ for ingestion by the Discovery_Engine core.

Cross-Media RDF Linking: When processing image_metadata and video_index entries,
automatically construct semantic RDF triples binding abstract concepts to visual
keys, screenshots, and video timestamp chunks via W3C prov:hadPrimarySource and
skos:related predicate relationships.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

INTAKE_DIR = Path(__file__).parent / "Intake_Queue"
PROCESSED_DIR = Path(__file__).parent / "Processed_Gate" / "normalized_triples"
REPORT_DIR = Path(__file__).resolve().parent.parent / "Bridge" / "out" / "aggregator_reports"

# W3C PROV-O and SKOS namespace prefixes for RDF output
PREFIXES = """@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
"""

# Import bus_manager for transaction logging to Bridge/messages.jsonl
try:
    from Bridge.bus_manager import post_message
    BUS_MANAGER_AVAILABLE = True
except ImportError:
    BUS_MANAGER_AVAILABLE = False

CATEGORY_SCHEMA_KEYS = {
'''

with open(filepath, "w") as f:
    f.write(part1)

print("Part 1 done")