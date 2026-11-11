"""Script to create complete intake_processor.py with cross-media RDF linking"""

import os

os.chdir("C:/Users/crmte/OneDrive/Desktop/Projects/Discovery_Engine")

# Write the complete file
filepath = "05_Knowledge_Aggregator/intake_processor.py"

content = '''"""
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
    "raw_cognitive_models": ["metadata", "entities", "relations", "invariants"],
    "structural_analogies": ["analogy_id", "source_domain", "target_domain", "mappings"],
    "conceptual_schemes": ["scheme_id", "title", "keywords", "concepts"],
    "image_metadata": ["image_id", "source_path_or_url", "extracted_concepts", "prov", "confidence_score", "skos"],
    "video_index": ["video_id", "source_path_or_url", "temporal_chunks", "prov", "confidence_score", "skos"],
}

ENTITY_REQUIRED_KEYS = ["id", "name", "type", "properties"]
RELATION_REQUIRED_KEYS = ["subject", "predicate", "object"]
MAPPING_REQUIRED_KEYS = ["source_element", "target_element", "relation_type"]
CONCEPT_REQUIRED_KEYS = ["name", "definition"]
'''

with open(filepath, "w") as f:
    f.write(content)

print("Base file written")
'''

print("Starting script creation")