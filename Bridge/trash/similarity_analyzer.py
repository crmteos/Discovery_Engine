#!/usr/bin/env python3
"""Hybrid Cosine Similarity Analyzer - Dual Mode A (TF-IDF) and Mode B (Dense Semantic Embeddings)"""
import json, os, hashlib
from datetime import datetime, timezone
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parent
BRIDGE_DIR = PROJECT_ROOT.parent / "Bridge"
REPORT_DIR = BRIDGE_DIR / "out" / "aggregator_reports"

class HybridSimilarityAnalyzer:
    """Dual-mode hybrid cosine similarity engine for draft deduplication and cross-media linking."""

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 3),
            lowercase=True,
        )
        self.semantic_model_available = False
        self._try_load_semantic_model()

    def _try_load_semantic_model(self):
        """Try to load local sentence-transformers model."""
        try:
            from sentence_transformers import SentenceTransformer

            self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.semantic_model_available = True
        except ImportError:
            self.semantic_model_available = False

    def compute_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Calculate TF-IDF cosine similarity between two texts."""
        if not text1 or not text2:
            return 0.0
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.0

    def compute_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate dense semantic cosine similarity using local embedding vectors."""
        if not text1 or not text2:
            return 0.0
        if not self.semantic_model_available:
            return 0.0
        try:
            embeddings = self.sentence_model.encode([text1, text2])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
        except Exception:
            return 0.0

    def check_deduplication(
        self, draft_payload: dict, existing_drafts: list, threshold: float = 0.90
    ) -> bool:
        """Check if a draft is a high-similarity duplicate of existing drafts."""
        draft_text = self._extract_text_for_comparison(draft_payload)

        if not draft_text:
            return False

        for existing in existing_drafts:
            existing_text = self._extract_text_for_comparison(existing)
            if not existing_text:
                continue

            # Mode A: TF-IDF fast screening
            tfidf_score = self.compute_tfidf_similarity(draft_text, existing_text)
            if tfidf_score >= threshold:
                return True

            # Mode B: Semantic similarity for near-duplicates
            if self.semantic_model_available:
                semantic_score = self.compute_semantic_similarity(draft_text, existing_text)
                if semantic_score >= threshold:
                    return True

        return False

    def _extract_text_for_comparison(self, payload: dict) -> str:
        """Extract comparable text from a draft payload."""
        text_fields = ["title", "content", "summary", "description", "text", "model_name"]
        for field in text_fields:
            if field in payload and payload[field]:
                text = str(payload[field])
                if len(text.strip()) > 3:
                    return text
        concatenated = " ".join(
            str(v) for v in payload.values() if isinstance(v, str) and len(v.strip()) > 3
        )
        if concatenated:
            return concatenated
        return ""

    def find_cross_media_links(
        self, concept_text: str, media_items: list, threshold: float = 0.75
    ) -> list:
        """Identify relevant media items for automatic skos:related RDF triple generation."""
        if not concept_text or not media_items:
            return []

        linked_items = []
        concept_clean = concept_text.strip()

        for media_item in media_items:
            media_desc = media_item.get("description", "")
            media_type = media_item.get("media_type", "unknown")

            if not media_desc:
                continue

            # Mode A: TF-IDF similarity
            tfidf_score = self.compute_tfidf_similarity(concept_clean, media_desc)

            # Mode B: Semantic similarity
            semantic_score = 0.0
            if self.semantic_model_available:
                semantic_score = self.compute_semantic_similarity(concept_clean, media_desc)

            combined_score = max(tfidf_score, semantic_score)

            if combined_score >= threshold:
                linked_item = {
                    "media_item": media_item,
                    "similarity_score": round(combined_score, 4),
                    "link_type": "skos:related",
                    "media_type": media_type,
                }
                linked_items.append(linked_item)

        linked_items.sort(key=lambda x: x["similarity_score"], reverse=True)
        return linked_items

    def generate_deduplication_log(self, is_duplicate: bool, draft_payload: dict) -> dict:
        """Generate a deduplication event log entry for bus messaging."""
        return {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "task_id": hashlib.sha256(
                f"{datetime.now(timezone.utc)}{uuid.uuid4()}".encode()
            ).hexdigest()[:16],
            "action": "deduplication_check",
            "payload": {
                "is_duplicate": is_duplicate,
                "draft_id": draft_payload.get("id", "unknown"),
            },
            "idempotency_key": hashlib.sha256(
                f"{datetime.now(timezone.utc)}{uuid.uuid4()}".encode()
            ).hexdigest()[:16],
        }

    def generate_cross_media_link_log(self, linked_items: list, concept_text: str) -> dict:
        """Generate cross-media linking event log entry for bus messaging."""
        return {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "task_id": hashlib.sha256(
                f"{datetime.now(timezone.utc)}{uuid.uuid4()}".encode()
            ).hexdigest()[:16],
            "action": "cross_media_linking",
            "payload": {
                "concept_text": concept_text,
                "linked_media_count": len(linked_items),
                "links": [
                    {
                        "media_id": item["media_item"].get("id", "unknown"),
                        "media_type": item["media_type"],
                        "similarity_score": item["similarity_score"],
                        "link_type": item["link_type"],
                    }
                    for item in linked_items
                ],
            },
            "idempotency_key": hashlib.sha256(
                f"{datetime.now(timezone.utc)}{uuid.uuid4()}".encode()
            ).hexdigest()[:16],
        }


def run_deduplication_check(draft_payload: dict, existing_drafts: list, threshold: float = 0.90) -> dict:
    """Convenience function to run deduplication check and return result with logging."""
    analyzer = HybridSimilarityAnalyzer()
    is_duplicate = analyzer.check_deduplication(draft_payload, existing_drafts, threshold)
    log_entry = analyzer.generate_deduplication_log(is_duplicate, draft_payload)
    return {"is_duplicate": is_duplicate, "log_entry": log_entry}


def run_cross_media_linking(
    concept_text: str, media_items: list, threshold: float = 0.75
) -> dict:
    """Convenience function to run cross-media linking and return results with logging."""
    analyzer = HybridSimilarityAnalyzer()
    linked_items = analyzer.find_cross_media_links(concept_text, media_items, threshold)
    log_entry = analyzer.generate_cross_media_link_log(linked_items, concept_text)
    return {"linked_items": linked_items, "log_entry": log_entry}


if __name__ == "__main__":
    """Simple smoke test when run directly."""
    import uuid

    analyzer = HybridSimilarityAnalyzer()

    print("=== Hybrid Similarity Analyzer Smoke Test ===\n")

    # Test Mode A: TF-IDF similarity
    text1 = "The cognitive model represents entity relationships in knowledge graphs"
    text2 = "The cognitive model represents entity relationships in knowledge graphs"

    score_a = analyzer.compute_tfidf_similarity(text1, text2)
    print(f"Mode A (TF-IDF) identical texts: {score_a:.4f} (expected: ~1.0)")

    text3 = "Image processing techniques for feature extraction"
    text4 = "Video compression algorithms for streaming efficiency"
    score_a2 = analyzer.compute_tfidf_similarity(text3, text4)
    print(f"Mode A (TF-IDF) different texts: {score_a2:.4f} (expected: low)")

    # Test Mode B: Semantic similarity
    if analyzer.semantic_model_available:
        score_b = analyzer.compute_semantic_similarity(text1, text2)
        print(f"Mode B (Semantic) identical texts: {score_b:.4f}")
    else:
        print("Mode B: Semantic model not available, skipping test")

    # Test deduplication
    draft = {"id": "draft_001", "title": "Cognitive model for entity relationships", "content": "The cognitive model represents entity relationships in knowledge graphs"}
    existing = [
        {"id": "draft_002", "title": "Cognitive model for entity relationships", "content": "The cognitive model represents entity relationships in knowledge graphs"}
    ]
    result = analyzer.check_deduplication(draft, existing, threshold=0.90)
    print(f"Deduplication check (identical): {result} (expected: True)")

    # Test cross-media linking
    media_items = [
        {"id": "img_001", "media_type": "image", "description": " diagram showing entity relationships in cognitive models"},
        {"id": "vid_001", "media_type": "video", "description": " tutorial on knowledge graph construction"},
    ]
    cross_result = analyzer.find_cross_media_links(
        "entity relationships in knowledge graphs", media_items, threshold=0.75
    )
    print(f"Cross-media links found: {len(cross_result)}")
    for item in cross_result:
        print(f"  - {item['media_item']['media_type']}: score={item['similarity_score']:.4f}")

    print("\n=== Smoke Test Complete ===")