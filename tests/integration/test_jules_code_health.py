"""Integration test for Jules Code Health script (`scripts/jules_code_health.py`).

Verifies that the script runs successfully in `--check` mode,
exits with code 0, and produces a valid JSON report.
"""

import json
import subprocess
import sys

import pytest


SCRIPT_PATH = str(
    __file__.rsplit("/", 2)[0] + "/scripts/jules_code_health.py"
    if "/" in __file__
    else "scripts/jules_code_health.py"
)
# More robust: use absolute path relative to project root
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


def test_jules_code_health_check_exit_code():
    """--check should exit with code 0."""
    exit_code, _ = run_jules_check()
    assert exit_code == 0, f"Expected exit_code 0, got {exit_code}"


def test_jules_code_health_report_valid():
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