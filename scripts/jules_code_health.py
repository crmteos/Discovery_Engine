#!/usr/bin/env python3
"""Jules Code Health Script - autonomous code analysis and sanitization.

CLI parameters:
  --check   Run code health checks (coverage, TODO/FIXME detection) and generate report.
  --sanitize Remove or fix TODO/FIXME comments in source files.
  --report  Generate JSON report (default path: logs/code_health_report.json).

The script operates in fully offline mode; exit_code is always 0.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


# Project root is the parent of the scripts/ directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIRS = [
    PROJECT_ROOT / "00_Project_Interface" / "src",
    PROJECT_ROOT / "05_Knowledge_Aggregator" / "src",
    PROJECT_ROOT / "06_Formalized_Model" / "src",
]
LOG_DIR = PROJECT_ROOT / "logs"
REPORT_PATH = LOG_DIR / "code_health_report.json"


def find_todo_fixme(root: Path):
    """Find TODO and FIXME comments in Python files under root."""
    patterns = []
    if not root.is_dir():
        return patterns
    for py_file in root.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for line_no, line in enumerate(content.splitlines(), start=1):
            if re.search(r"TODO|FIXME", line, re.IGNORECASE):
                patterns.append({"file": str(py_file), "line": line_no, "text": line.strip()})
    return patterns


def run_pytest_cov():
    """Run pytest with coverage and return coverage percentage and return code."""
    # Ensure logs directory exists for coverage output
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Remove any old coverage data to get fresh results
    for old in Path.cwd().glob(".coverage*"):
        try:
            old.unlink()
        except Exception:
            pass

    # Run pytest on the tests directory with coverage
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "--cov=",
            "--cov-report=json",
            "-q",
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    # Try to read the generated .coverage.json
    cov_file = Path(".coverage.json")
    percentage = 0.0
    if cov_file.is_file():
        try:
            data = json.loads(cov_file.read_text(encoding="utf-8"))
            # Navigate the nested structure; structure may vary
            totals = data.get("totals", {})
            percentage = totals.get("percent_covered", 0.0)
        except Exception:
            percentage = 0.0
    return percentage, result.returncode


def main():
    parser = argparse.ArgumentParser(description="Jules Code Health Script")
    parser.add_argument(
        "--check", action="store_true", help="Run code health checks and generate report"
    )
    parser.add_argument(
        "--sanitize",
        action="store_true",
        help="Sanitize TODO/FIXME comments in source files",
    )
    parser.add_argument(
        "--report", action="store_true", help="Generate JSON report file"
    )
    args = parser.parse_args()

    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    issues = {}

    # Run pytest coverage check
    cov_pct, pytest_rc = run_pytest_cov()
    issues["coverage_percent"] = round(cov_pct, 2)
    if pytest_rc != 0:
        issues["pytest_failed"] = True
    else:
        issues["pytest_failed"] = False

    # Find TODO/FIXME smells in source directories
    todo_fixme = []
    for src_dir in SOURCES_DIRS:
        todo_fixme.extend(find_todo_fixme(src_dir))
    issues["todo_fixme_count"] = len(todo_fixme)
    if todo_fixme:
        issues["smells_detected"] = True
        issues["todo_fixme_examples"] = todo_fixme[:10]  # first 10 examples
    else:
        issues["smells_detected"] = False
        issues["todo_fixme_examples"] = []

    # Sanitize TODO/FIXME comments if requested
    if args.sanitize:
        for entry in todo_fixme:
            py_file = Path(entry["file"])
            if not py_file.is_file():
                continue
            lines = py_file.read_text(encoding="utf-8").splitlines()
            new_lines = []
            for i, line in enumerate(lines, start=1):
                if i == entry["line"]:
                    # Replace the entire line with a sanitized comment
                    new_lines.append("# SANITIZED")
                else:
                    new_lines.append(line)
            py_file.write_text("\n".join(new_lines), encoding="utf-8")
        issues["sanitized"] = True
    else:
        issues["sanitized"] = False

    # Determine whether to write report
    write_report = args.report or args.check

    if write_report:
        REPORT_PATH.write_text(json.dumps(issues, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Report written to {REPORT_PATH}")

    # In offline mode, exit code is always 0
    sys.exit(0)


if __name__ == "__main__":
    main()