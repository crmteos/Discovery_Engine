# Cline Directive: Deploy Hybrid Cosine Similarity Analyzer & Auto-Deduplication Engine

## Target Subsystem
`05_Knowledge_Aggregator`

## Target Path
`C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`

---

## 1. Objective
Deploy `similarity_analyzer.py` under `05_Knowledge_Aggregator/` implementing a **dual-mode (Hybrid) Cosine Similarity Engine**:
1. **Mode A (Fast TF-IDF / Vectorizer):** High-speed deterministic duplicate screening and n-gram lexical similarity scoring using `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`).
2. **Mode B (Deep Semantic Embeddings):** Dense semantic vector embeddings using local `sentence-transformers` / `Ollama` embeddings for deep cross-media SKOS linking (`skos:related`) between text concepts, image metadata descriptions, and video transcripts.

Integrated seamlessly with `intake_processor.py` and `bus_manager.py` under a strict **$0.00 budget limit**.

---

## 2. Requirements & Architecture

### File to Create
`05_Knowledge_Aggregator/similarity_analyzer.py`

### Functional Specs
1. **`class HybridSimilarityAnalyzer`**:
   - `compute_tfidf_similarity(text1: str, text2: str) -> float`: Calculates TF-IDF cosine similarity. Returns score between `0.0` and `1.0`.
   - `compute_semantic_similarity(text1: str, text2: str) -> float`: Fallback/dense semantic cosine similarity using local embedding vectors.
   - `check_deduplication(draft_payload: dict, existing_drafts: list, threshold: float = 0.90) -> bool`: Returns `True` if high-similarity duplicate exists.
   - `find_cross_media_links(concept_text: str, media_items: list, threshold: float = 0.75) -> list`: Identifies relevant media items for automatic `skos:related` RDF triple generation.

2. **Integration with `intake_processor.py`**:
   - Before normalizing a draft, run `check_deduplication()`. If duplicate is detected (`similarity >= 0.90`), flag draft status as `DUPLICATE_SKIPPED` and log event to `Bridge/messages.jsonl`.
   - During triple generation, run `find_cross_media_links()` to auto-link concept nodes with `image_metadata` and `video_index` nodes (`skos:related`).

3. **Smoke Test & Verification**:
   - Create a test script `test_similarity.py` in `05_Knowledge_Aggregator/` to test both Mode A and Mode B algorithms on sample drafts.
   - Run `bus_inspector.py` to confirm zero bus errors.

4. **Execution Report**:
   - Save execution report to `Bridge/out/aggregator_reports/report_similarity_analyzer_[TIMESTAMP].md`.

---

## 3. Verification & Acceptance Criteria
- [ ] `similarity_analyzer.py` compiles with `exit_code: 0`.
- [ ] Both Mode A (TF-IDF) and Mode B (Dense Semantic Embeddings) execute locally without external API calls.
- [ ] Deduplication threshold detection (>= 0.90) correctly flags identical/near-identical drafts.
- [ ] Cross-media linking threshold (>= 0.75) correctly outputs `skos:related` RDF triples.
- [ ] `bus_inspector.py` audit passes with 0 errors.
- [ ] Execution report saved to `Bridge/out/aggregator_reports/report_similarity_analyzer_[TIMESTAMP].md`.
- [ ] Total cost strictly **$0.00**.
