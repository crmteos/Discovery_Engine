"""Integration test for Jules Code Health script (`scripts/jules_code_health.py`).

Verifies that the script runs successfully in `--check`, `--report`, and `--sync-state`
modes, exits with code 0, and produces valid JSON reports.
"""

import json
import os
import subprocess
import sys

import pytest

PROJECT_ROOT = "c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine"
SCRIPT_ABS = f"{PROJECT_ROOT}\\scripts\\jules_code_health.py"


def run_jules_check():
    """Run jules_code_health.py with --check and return (exit_code, report_path)."""
    report_path = f"{PROJECT_ROOT}\\logs\\code_health_report.json"
    # Remove old report if exists to get a fresh one
    try:
        os.remove(report_path)
    except FileNotFoundError:
        pass
    result = subprocess.run(
        [sys.executable, SCRIPT_ABS, "--check"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    return result.returncode, report_path


def run_jules_report():
    """Run jules_code_health.py with --report and return (exit_code, report_path)."""
    report_path = f"{PROJECT_ROOT}\\logs\\code_health_report.json"
    try:
        os.remove(report_path)
    except FileNotFoundError:
        pass
    result = subprocess.run(
        [sys.executable, SCRIPT_ABS, "--report"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    return result.returncode, report_path


def run_jules_sync():
    """Run jules_code_health.py with --sync-state and return exit_code."""
    result = subprocess.run(
        [sys.executable, SCRIPT_ABS, "--sync-state"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    return result.returncode


def test_code_health_check_exit_code():
    """--check should exit with code 0."""
    exit_code, _ = run_jules_check()
    assert exit_code == 0, f"Expected exit_code 0, got {exit_code}"


def test_code_health_check_report_valid():
    """--check should produce a valid JSON report with expected keys."""
    exit_code, report_path = run_jules_check()
    assert exit_code == 0
    # Report should exist
    assert os.path.isfile(report_path), f"Report file not found at {report_path}"
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    # Expect coverage_percent and smells_detected at minimum
    assert "coverage_percent" in report, "Report missing 'coverage_percent'"
    assert "smells_detected" in report, "Report missing 'smells_detected'"
    assert "todo_fixme_count" in report, "Report missing 'todo_fixme_count'"


def test_code_health_report_generation():
    """--report should generate the JSON report file."""
    exit_code, report_path = run_jules_report()
    assert exit_code == 0
    assert os.path.isfile(report_path), "Report file not generated"


def test_code_health_sync_exit_code():
    """--sync-state should exit with code 0."""
    exit_code = run_jules_sync()
    assert exit_code == 0, f"Expected exit_code 0 for --sync-state, got {exit_code}"


def test_code_health_sync_updates_project_state():
    """--sync-state should update PROJECT_STATE.md with code health metrics."""
    # First run --check to generate report
    exit_code, report_path = run_jules_check()
    assert exit_code == 0
    # Then run --sync-state
    exit_code = run_jules_sync()
    assert exit_code == 0
    # Verify that PROJECT_STATE.md contains the synced section
    state_path = f"{PROJECT_ROOT}\\PROJECT_STATE.md"
    assert os.path.isfile(state_path), "PROJECT_STATE.md not found"
    with open(state_path, "r", encoding="utf-8") as f:
        content = f.read()
    marker = "### Code Health & Verification (auto-synced)"
    assert marker in content, f"Synced code health section not found in {state_path}"