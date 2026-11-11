#!/usr/bin/env python3
"""
Intake Processor: Validates incoming cognitive models and maps them into 01_Formal_Core.

Handles five intake categories:
  - raw_cognitive_models   -> cognitive_model_template.json schema
  - structural_analogies   -> analogy_template.json schema
  - conceptual_schemes     -> concept_scheme_template.json schema
  - image_metadata         -> image_metadata_template.json schema
  - video_index            -> video_index_template.json schema

import json
import os
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Import hybrid similarity analyzer for deduplication and cross-media linking
from similarity_analyzer import HybridSimilarityAnalyzer

# Resolve paths relative to this script
PROJECT_ROOT = Path(__file__).resolve().parent
INTAKE_DIR = PROJECT_ROOT / "Intake_Queue"
PROCESSED_DIR = PROJECT_ROOT / "Processed_Gate" / "normalized_triples"
REPORT_DIR = PROJECT_ROOT.parent / "Bridge" / "out" / "aggregator_reports"

# Ensure output directories exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Import bus_manager for transaction logging to Bridge/messages.jsonl
try:
    from Bridge.bus_manager import post_message
    BUS_MANAGER_AVAILABLE = True
except ImportError:
    BUS_MANAGER_AVAILABLE = False

# Category schema key mappings (matching schema_validator.py TEMPLATE_MAP)
CATEGORY_SCHEMA_KEYS = {
    "raw_cognitive_models": ["metadata", "entities", "relations", "invariants"],
    "structural_analogies": ["analogy_id", "source_domain", "target_domain", "mappings"],
    "conceptual_schemes": ["scheme_id", "title", "keywords", "concepts"],
    "image_metadata": ["image_id", "source_path_or_url", "extracted_concepts", "prov", "confidence_score", "skos"],
    "video_index": ["video_id", "source_path_or_url", "temporal_chunks", "prov", "confidence_score", "skos"],
}

# Required key sets for validation
def _generate_message_id():
    """Generate a unique SHA256-based message ID for bus logging."""
    return hashlib.sha256(f"{datetime.now(timezone.utc)}{uuid.uuid4()}".encode()).hexdigest()[:16]


def _check_deduplication(draft_payload: dict, existing_drafts: list) -> dict:
    """Check if a draft is a duplicate using hybrid similarity analyzer.

    Returns dict with 'is_duplicate' bool and 'similarity_score' float.
    If duplicate, also returns 'deduplication_reason' string.
    """
    analyzer = HybridSimilarityAnalyzer()
    result = analyzer.check_deduplication(draft_payload, existing_drafts, threshold=0.90)
    similarity_score = 0.0
    if result and "draft_payload" in locals():
        # Calculate the actual similarity score for logging
        draft_text = analyzer._extract_text_for_comparison(draft_payload)
        if draft_text:
            for existing in existing_drafts:
                existing_text = analyzer._extract_text_for_comparison(existing)
                if existing_text:
                    score = analyzer.compute_tfidf_similarity(draft_text, existing_text)
                    if score >= 0.90:
                        similarity_score = score
                        break
    return {"is_duplicate": result, "similarity_score": similarity_score}


# Log deduplication event to bus
def _log_deduplication_event(is_duplicate: bool, draft_payload: dict, existing_drafts: list):
    """Log deduplication check result to Bridge messages.jsonl."""
    if not BUS_MANAGER_AVAILABLE:
        return

    analyzer = HybridSimilarityAnalyzer()
    dedup_result = _check_deduplication(draft_payload, existing_drafts)

    if dedup_result["is_duplicate"]:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "task_id": hashlib.sha256(
                f"{datetime.now(timezone.utc)}{uuid.uuid4()}".encode()
            ).hexdigest()[:16],
            "action": "deduplication_check",
            "payload": {
                "draft_id": draft_payload.get("id", "unknown"),
                "is_duplicate": True,
                "similarity_score": round(dedup_result["similarity_score"], 4),
                "duplicate_reason": "High-similarity duplicate detected via TF-IDF/semantic analysis",
            },
            "idempotency_key": hashlib.sha256(
                f"{datetime.now(timezone.utc)}{uuid.uuid4()}".encode()
            ).hexdigest()[:16],
        }
        try:
            from Bridge.bus_manager import post_message
            post_message(log_entry)
        except Exception as e:
            print(f"Warning: Failed to log deduplication event: {e}")


def _generate_rdf_triples_from_cognitive_model(data, task_id=None):
    """Generate normalized W3C PROV-O / SKOS RDF triples from a cognitive model draft."""
    entities = data.get("entities", [])
    relations = data.get("relations", [])
    metadata = data.get("metadata", {})

    triples = []

    # PROV-O: attribution and generation
    agent = metadata.get("author", "unknown")
    timestamp = metadata.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    for entity in entities:
        eid = entity.get("id", " Unknown Entity ID")
        name = entity.get("name", "Unknown")
        ent_type = entity.get("type", "Unknown")

        # PROV-O wasAttributedTo for the entity
        triple = {
            "subject": eid,
            "predicate": "prov:wasAttributedTo",
            "object": f"agg:{agent.lower().replace(' ', '')}",
            "type": "triple",
        }
        triples.append(triple)

        # SKOS prefLabel
        triple = {
            "subject": eid,
            "predicate": "skos:prefLabel",
            "object": name,
            "type": "triple",
        }
        triples.append(triple)

    # PROV-O: generatedAtTime at the model level
    triple = {
        "subject": metadata.get("model_name", "unknown_model"),
        "predicate": "prov:generatedAtTime",
        "object": timestamp,
        "type": "triple",
    }
    triples.append(triple)

    # Relations as rdf:statements or skos:related
    for rel in relations:
        subj = rel.get("subject", "")
        pred = rel.get("predicate", "")
        obj = rel.get("object", "")

        triple = {
            "subject": subj,
            "predicate": pred,
            "object": obj,
            "type": "triple",
        }
        triples.append(triple)

    def _generate_rdf_triples_from_image_metadata(data, task_id=None):
    """Generate normalized W3C PROV-O / SKOS RDF triples from an image metadata draft."""
    image_id = data.get("image_id", "unknown_image")
    extracted_concepts = data.get("extracted_concepts", [])
    prov = data.get("prov", {})
    skos = data.get("skos", {})
    confidence = data.get("confidence_score", 1.0)
    visual_keys = data.get("visual_keys", [])
    source_path = data.get("source_path_or_url", "")

    triples = []

    # PROV-O: wasAttributedTo
    agent = prov.get("wasAttributedTo", "unknown")
    triple = {
        "subject": image_id,
        "predicate": "prov:wasAttributedTo",
        "object": f"agg:{agent.lower().replace(' ', '')}",
        "type": "triple",
    }
    triples.append(triple)

    # PROV-O: generatedAtTime
    generated_at = prov.get("generatedAtTime", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    triple = {
        "subject": image_id,
        "predicate": "prov:generatedAtTime",
        "object": generated_at,
        "type": "triple",
    }
    triples.append(triple)

    # PROV-O: hadPrimarySource
    primary_source = prov.get("hadPrimarySource", source_path)
    triple = {
        "subject": image_id,
        "predicate": "prov:hadPrimarySource",
        "object": primary_source,
        "type": "triple",
    }
    triples.append(triple)

    # SKOS concepts with prefLabel and broader/narrower/related
    for concept in extracted_concepts:
        concept_name = concept.get("concept_name", "unknown")
        definition = concept.get("definition", "")

        # skos:prefLabel
        triple = {
            "subject": f":{concept_name}",
            "predicate": "skos:prefLabel",
            "object": concept_name,
            "type": "triple",
        }
        triples.append(triple)

        if definition:
            triple = {
                "subject": f":{concept_name}",
                "predicate": "skos:definition",
                "object": definition,
                "type": "triple",
            }
            triples.append(triple)

        # skos:broader if available
        if "broader" in concept:
            triple = {
                "subject": f":{concept_name}",
                "predicate": "skos:broader",
                "object": concept["broader"],
                "type": "triple",
            }
            triples.append(triple)

        # skos:narrower if available
        if "narrower" in concept:
            for narrower in concept["narrower"]:
                triple = {
                    "subject": f":{concept_name}",
                    "predicate": "skos:narrower",
                    "object": narrower,
                    "type": "triple",
                }
                triples.append(triple)

        # skos:related if available
        if "related" in concept:
            for related in concept["related"]:
                triple = {
                    "subject": f":{concept_name}",
                    "predicate": "skos:related",
                    "object": related,
                    "type": "triple",
                }
                triples.append(triple)

    def _generate_rdf_triples_from_video_index(data, task_id=None):
    """Generate normalized W3C PROV-O / SKOS RDF triples from a video index draft."""
    video_id = data.get("video_id", "unknown_video")
    temporal_chunks = data.get("temporal_chunks", [])
    prov = data.get("prov", {})
    skos = data.get("skos", {})
    confidence = data.get("confidence_score", 1.0)
    source_path = data.get("source_path_or_url", "")

    triples = []

    # PROV-O: wasAttributedTo
    agent = prov.get("wasAttributedTo", "unknown")
    triple = {
        "subject": video_id,
        "predicate": "prov:wasAttributedTo",
        "object": f"agg:{agent.lower().replace(' ', '')}",
        "type": "triple",
    }
    triples.append(triple)

    # PROV-O: generatedAtTime
    generated_at = prov.get("generatedAtTime", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    triple = {
        "subject": video_id,
        "predicate": "prov:generatedAtTime",
        "object": generated_at,
        "type": "triple",
    }
    triples.append(triple)

    # PROV-O: hadPrimarySource
    primary_source = prov.get("hadPrimarySource", source_path)
    triple = {
        "subject": video_id,
        "predicate": "prov:hadPrimarySource",
        "object": primary_source,
        "type": "triple",
    }
    triples.append(triple)

    # Process temporal chunks
    for i, chunk in enumerate(temporal_chunks):
        chunk_id = chunk.get("chunk_id", f"chunk_{i}")
        timestamp_start = chunk.get("timestamp_start", "00:00")
        timestamp_end = chunk.get("timestamp_end", "01:00")
        extracted_entities = chunk.get("extracted_entities", [])
        visual_keys = chunk.get("visual_keys", [])

        # Triple for the chunk itself
        triple = {
            "subject": f"{video_id}_{chunk_id}",
            "predicate": "prov:generatedAtTime",
            "object": f"{timestamp_start}-{timestamp_end}",
            "type": "triple",
        }
        triples.append(triple)

        # PROV-O: hadPrimarySource for chunk
        triple = {
            "subject": f"{video_id}_{chunk_id}",
            "predicate": "prov:hadPrimarySource",
            "object": primary_source,
            "type": "triple",
        }
        triples.append(triple)

        # SKOS concepts within chunk
        for entity in extracted_entities:
            triple = {
                "subject": f"{video_id}_{chunk_id}",
                "predicate": "skos:prefLabel",
                "object": entity,
                "type": "triple",
            }
            triples.append(triple)

        # Visual keys
        for j, visual_key in enumerate(visual_keys):
            triple = {
                "subject": f"{video_id}_{chunk_id}",
                "predicate": "skos:related",
                "object": f"{visual_key}",
                "type": "triple",
            }
            triples.append(triple)

    def _validate_image_metadata(data):
    """Validate image metadata against its contract schema."""
    errors = []

    # Required root fields
    required_fields = ["image_id", "source_path_or_url", "extracted_concepts", "prov", "confidence_score"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # PROV-O compliance
    prov = data.get("prov", {})
    prov_fields = ["prov:wasAttributedTo", "prov:generatedAtTime", "prov:hadPrimarySource"]
    for field in prov_fields:
        if field not in prov:
            errors.append(f"Missing PROV-O field in 'prov': '{field}'")

    # confidence_score should be a number between 0 and 1
    confidence = data.get("confidence_score")
    if confidence is not None:
        try:
            conf_val = float(confidence)
            if conf_val < 0 or conf_val > 1:
                errors.append(f"confidence_score must be between 0 and 1, got {confidence}")
        except (ValueError, TypeError):
            errors.append(f"confidence_score must be a number, got {confidence}")

    # SKOS compliance
    skos = data.get("skos", {})
    skos_fields = ["broader", "related", "prefLabel"]
    for field in skos_fields:
        if field not in skos and not any(
            field in c for c in data.get("extracted_concepts", [])
        ):
            pass  # SKOS fields can be at concept level; not strictly required at top level

    return errors


def _validate_video_index(data):
    """Validate video index against its contract schema."""
    errors = []

    # Required root fields
    required_fields = ["video_id", "source_path_or_url", "temporal_chunks", "prov", "confidence_score"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # PROV-O compliance
    prov = data.get("prov", {})
    prov_fields = ["prov:wasAttributedTo", "prov:generatedAtTime", "prov:hadPrimarySource"]
    for field in prov_fields:
        if field not in prov:
            errors.append(f"Missing PROV-O field in 'prov': '{field}'")

    # confidence_score validation
    confidence = data.get("confidence_score")
    if confidence is not None:
        try:
            conf_val = float(confidence)
            if conf_val < 0 or conf_val > 1:
                errors.append(f"confidence_score must be between 0 and 1, got {confidence}")
        except (ValueError, TypeError):
            errors.append(f"confidence_score must be a number, got {confidence}")

    def _process_structural_analogy(data, task_id=None):
    """Generate RDF triples from a structural analogy draft."""
    analogy_id = data.get("analogy_id", "unknown_analogy")
    source_domain = data.get("source_domain", "")
    target_domain = data.get("target_domain", "")
    mappings = data.get("mappings", [])

    triples = []

    # PROV-O attribution
    agent = "aggregator"
    triple = {
        "subject": analogy_id,
        "predicate": "prov:wasAttributedTo",
        "object": f"agg:{agent.lower().replace(' ', '')}",
        "type": "triple",
    }
    triples.append(triple)

    triple = {
        "subject": analogy_id,
        "predicate": "prov:generatedAtTime",
        "object": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": "triple",
    }
    triples.append(triple)

    # SKOS: source_domain and target_domain as concepts
    if source_domain:
        triple = {
            "subject": f":{source_domain}",
            "predicate": "skos:prefLabel",
            "object": source_domain,
            "type": "triple",
        }
        triples.append(triple)

    if target_domain:
        triple = {
            "subject": f":{target_domain}",
            "predicate": "skos:prefLabel",
            "object": target_domain,
            "type": "triple",
        }
        triples.append(triple)

    # Mapping as skos:related relationships
    for i, mapping in enumerate(mappings):
        source_elem = mapping.get("source_element", "")
        target_elem = mapping.get("target_element", "")
        relation_type = mapping.get("relation_type", "related")

        triple = {
            "subject": f":{source_elem}",
            "predicate": f"maps_to_{relation_type}",
            "object": f":{target_elem}",
            "type": "triple",
        }
        triples.append(triple)

    if task_id is None:
        task_id = _generate_message_id()

    return {
        "category": "structural_analogies",
        "input_model": analogy_id,
        "rdf_triples": triples,
        "task_id": task_id,
        "output_location": str(PROCESSED_DIR / f"structural_analogy_{analogy_id}.json"),
    }


def _process_conceptual_scheme(data, task_id=None):
    """Generate RDF triples from a conceptual scheme draft."""
    scheme_id = data.get("scheme_id", "unknown_scheme")
    title = data.get("title", "")
    keywords = data.get("keywords", [])
    concepts = data.get("concepts", [])

    triples = []

    # PROV-O attribution
    triple = {
        "subject": scheme_id,
        "predicate": "prov:wasAttributedTo",
        "object": "agg:aggregator",
        "type": "triple",
    }
    triples.append(triple)

    triple = {
        "subject": scheme_id,
        "predicate": "prov:generatedAtTime",
        "object": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": "triple",
    }
    triples.append(triple)

    # SKOS: scheme prefLabel
    if title:
        triple = {
            "subject": scheme_id,
            "predicate": "skos:prefLabel",
            "object": title,
            "type": "triple",
        }
        triples.append(triple)

    # SKOS: keywords
    for i, keyword in enumerate(keywords):
        triple = {
            "subject": scheme_id,
            "predicate": f"skos:altLabel[{i+1}]",
            "object": keyword,
            "type": "triple",
        }
        triples.append(triple)

    # SKOS concepts with prefLabel and broader/narrower/related
    for i, concept in enumerate(concepts):
        concept_name = concept.get("name", "unknown")
        definition = concept.get("definition", "")

        triple = {
            "subject": f":{concept_name}",
            "predicate": "skos:prefLabel",
            "object": concept_name,
            "type": "triple",
        }
        triples.append(triple)

        if definition:
            triple = {
                "subject": f":{concept_name}",
                "predicate": "skos:definition",
                "object": definition,
                "type": "triple",
            }
            triples.append(triple)

    if task_id is None:
        task_id = _generate_message_id()

    return {
        "category": "conceptual_schemes",
        "input_model": scheme_id,
        "rdf_triples": triples,
        "task_id": task_id,
        "output_location": str(PROCESSED_DIR / f"conceptual_scheme_{scheme_id}.json"),
    }