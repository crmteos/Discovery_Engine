#!/usr/bin/env python3
"""Integration test for Phase 45: BigQuery Agent Search."""

import json
import os
import subprocess
import sys
from pathlib import Path

# Project root setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = PROJECT_ROOT / "00_Project_Interface" / "src"
TESTS_DIR = PROJECT_ROOT / "tests" / "integration"

# Add project src to path
sys.path.insert(0, str(SRC_DIR))

from bigquery_agent_search import BigQueryAgentSearch, main


def test_py_compile():
    """Test syntax validity via py_compile."""
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(SRC_DIR / "bigquery_agent_search.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"py_compile failed: {result.stderr}"


def test_offline_fallback():
    """Test fallback execution mode with --offline flag."""
    result = subprocess.run(
        [sys.executable, str(SRC_DIR / "bigquery_agent_search.py"), "--query", "test query", "--offline"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Offline mode failed: {result.stderr}"
    # Verify exit_code: 0 in output
    assert "exit_code: 0" in result.stdout, f"Expected exit_code: 0 in output, got: {result.stdout}"


def test_json_structure():
    """Verify JSON structure and W3C PROV-O provenance preservation."""
    result = subprocess.run(
        [sys.executable, str(SRC_DIR / "bigquery_agent_search.py"), "--query", "test", "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"JSON mode failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert data.get("exit_code") == 0, f"exit_code should be 0, got: {data.get('exit_code')}"
    assert "mode" in data, "JSON output missing 'mode' key"
    assert "results" in data, "JSON output missing 'results' key"
    assert "query" in data, "JSON output missing 'query' key"
    # Verify PROV-O provenance is preserved
    for r in data.get("results", []):
        prov = r.get("prov", {})
        assert "@id" in prov, f"PROV-O entity missing '@id': {prov}"
        assert "@type" in prov, f"PROV-O entity missing '@type': {prov}"
        assert "prov:label" in prov, f"PROV-O entity missing 'prov:label': {prov}"


def test_exit_code_zero():
    """Enforce exit_code: 0 for zero-mock fallback verification."""
    # Test all execution paths return exit_code 0
    # Mode 1: offline
    r = subprocess.run(
        [sys.executable, str(SRC_DIR / "bigquery_agent_search.py"), "--query", "x", "--offline"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0 and "exit_code: 0" in r.stdout, "Offline mode must return exit_code: 0"

    # Mode 2: JSON output
    r = subprocess.run(
        [sys.executable, str(SRC_DIR / "bigquery_agent_search.py"), "--query", "x", "--json"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, "JSON mode must return exit_code: 0"
    data = json.loads(r.stdout)
    assert data.get("exit_code") == 0, "JSON output must have exit_code: 0"

    # Mode 3: default (offline fallback)
    r = subprocess.run(
        [sys.executable, str(SRC_DIR / "bigquery_agent_search.py"), "--query", "x"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, "Default mode must return exit_code: 0"