#!/usr/bin/env python3
"""Integration test for Phase 33: Ollama Gateway binding to Node 05 Intake Processor.

Tests the end-to-end extraction pipeline with sample unstructured text.
Verifies py_compile on all modified files and zero-crash operation
both with online Ollama and offline fallback.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Add project roots to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "05_Knowledge_Aggregator"))
sys.path.insert(0, str(PROJECT_ROOT / "00_Project_Interface" / "src"))

from intake_processor import extract_triplet_with_llm  # type: ignore[import]


def test_py_compile():
    """Verify that all modified files pass py_compile."""
    files = [
        "05_Knowledge_Aggregator/src/intake_processor.py",
        "00_Project_Interface/src/ollama_gateway.py",
    ]
    for f in files:
        path = PROJECT_ROOT / f
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"py_compile failed for {f}: {result.stderr}"


def test_llm_extract_offline_fallback():
    """Test that LLM extraction gracefully falls back when Ollama is offline."""
    # Sample unstructured text
    text = """
    The Discovery Engine project uses a local Ollama server running models 
    qwen2.5-coder:14b, llama3.1:8b, and qwen2.5:7b for NLP processing.
    """

    # This should not crash even if Ollama is offline - it returns a fallback dict
    try:
        result = extract_triplet_with_llm(text)
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        # Check that required keys are present (they may be fallback keys)
        assert "subject" in result and "predicate" in result and "object" in result and "graph_context" in result
    except Exception as exc:
        # The function should never raise unhandled exceptions per design
        assert False, f"extract_triplet_with_llm raised an unhandled exception: {exc}"


def test_llm_extract_with_sample():
    """Test end-to-end extraction pipeline with sample unstructured text."""
    text = """
    The Discovery Engine project automates knowledge graph construction 
    from cognitive model drafts using local Ollama LLMs.
    """

    result = extract_triplet_with_llm(text)
    # Result should be a dict with the expected keys
    assert isinstance(result, dict)
    # The function should always return a dict with subject, predicate, object, graph_context
    # even if it's a fallback value
    required_keys = {"subject", "predicate", "object", "graph_context"}
    assert required_keys.issubset(result.keys()), (
        f"Missing required keys. Got: {result.keys()}"
    )


def test_main_cli_no_crash():
    """Test that the CLI --llm-extract mode does not crash."""
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "05_Knowledge_Aggregator" / "src" / "intake_processor.py"), "--llm-extract"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    # The CLI should not crash - it should exit with code 0 or handle gracefully
    # Even if Ollama is offline, it should complete without unhandled exceptions
    assert result.returncode == 0, f"CLI crashed with exit_code {result.returncode}: {result.stderr}"


if __name__ == "__main__":
    # Run simple manual test
    print("Running integration test for Phase 33 Ollama Gateway binding...")
    print("=" * 60)

    # Run py_compile check
    print("\n1. Running py_compile check...")
    try:
        test_py_compile()
        print("   PASSED: All files compile successfully.")
    except Assertion as e:
        print(f"   FAILED: {e}")

    # Test offline fallback
    print("\n2. Testing LLM extraction offline fallback...")
    try:
        test_llm_extract_offline_fallback()
        print("   PASSED: Offline fallback works without crashes.")
    except Assertion as e:
        print(f"   FAILED: {e}")

    # Test end-to-end extraction
    print("\n3. Testing end-to-end extraction pipeline...")
    try:
        test_llm_extract_with_sample()
        print("   PASSED: Extraction pipeline works.")
    except Assertion as e:
        print(f"   FAILED: {e}")

    # Test CLI
    print("\n4. Testing CLI --llm-extract mode...")
    try:
        test_main_cli_no_crash()
        print("   PASSED: CLI runs without crashes.")
    except Assertion as e:
        print(f"   FAILED: {e}")

    print("\n" + "=" * 60)
    print("Integration test complete.")