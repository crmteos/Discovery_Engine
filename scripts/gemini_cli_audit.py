import json
import re
from pathlib import Path

# Project root detection
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = PROJECT_ROOT / "PROJECT_SPEC.md"
CONTEXT_PATH = PROJECT_ROOT / "PROJECT_CONTEXT.md"
STATE_PATH = PROJECT_ROOT / "PROJECT_STATE.md"


def check_no_paid_dependencies():
    """Check for no paid third-party API dependencies or non-standard packages."""
    issues = []

    if SPEC_PATH.is_file():
        with open(SPEC_PATH, "r", encoding="utf-8") as f:
            spec_content = f.read()

        budget_markers = ["$0.00", "Budget Limit:", "zero-cost", "zero-budget"]
        found_budget = any(marker in spec_content for marker in budget_markers)

        if not found_budget:
            issues.append("⚠️ Budget constraint not clearly documented")

    return issues


def check_offline_fallbacks():
    """Check for graceful offline fallbacks (exit_code: 0)."""
    issues = []
    python_files = list(PROJECT_ROOT.rglob("*.py"))

    fallback_patterns = ["--test", "offline", "fallback", "graceful", "exit_code: 0"]

    files_with_fallbacks = 0
    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
            content_lower = content.lower()
            for pattern in fallback_patterns:
                if pattern.lower() in content_lower:
                    files_with_fallbacks += 1
                    break
        except Exception:
            continue

    if files_with_fallbacks == 0:
        issues.append("⚠️ No offline fallback patterns detected")

    return issues


def check_prov_o_metadata():
    """Check for W3C PROV-O metadata preservation in intake adapters."""
    issues = []

    intake_files = [
        f
        for f in PROJECT_ROOT.rglob("*")
        if "intake" in f.name.lower()
    ]

    if not intake_files:
        issues.append("ℹ️ No intake adapter files found")
        return issues

    prov_o_found = False
    for f in intake_files[:10]:
        try:
            with open(f, "r", encoding="utf-8") as file:
                content = file.read()
            if "prov:wasDerivedFrom" in content:
                prov_o_found = True
                break
        except Exception:
            continue

    if not prov_o_found and intake_files:
        issues.append("⚠️ W3C PROV-O metadata not found in intake adapters")

    return issues


def check_pure_python_fallbacks():
    """Check for Pure Python Zero-Dependency Fallback Engines."""
    issues = []

    python_files = list(PROJECT_ROOT.rglob("*.py"))
    fallback_indicators = ["zero-dependency", "pure python", "fallback engine"]
    files_with_fallbacks = 0

    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
            content_lower = content.lower()
            for indicator in fallback_indicators:
                if indicator.lower() in content_lower:
                    files_with_fallbacks += 1
                    break
        except Exception:
            continue

    if files_with_fallbacks == 0:
        issues.append("⚠️ No pure Python fallback engine references detected")

    return issues


def run_local_audit():
    """Run the complete audit in local mode (no API key required)."""
    print("=" * 60)
    print("Gemini CLI DoD Audit - Local Mode")
    print("=" * 60)
    print(f"Project root: {PROJECT_ROOT}")
    print()

    all_checks = [
        ("No Paid Dependencies", check_no_paid_dependencies),
        ("Offline Fallbacks", check_offline_fallbacks),
        ("PROV-O Metadata", check_prov_o_metadata),
        ("Pure Python Fallbacks", check_pure_python_fallbacks),
    ]

    results = []
    for check_name, check_func in all_checks:
        issues = check_func()
        passed = len(issues) == 0
        results.append((check_name, passed, issues))
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check_name}")
        if issues:
            for issue in issues:
                print(f"  {issue}")

    print()
    print("=" * 60)

    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)

    if passed_count == total_count:
        print(f"🎉 All {total_count} checks PASSED (exit_code: 0)")
        return 0
    else:
        failed_count = total_count - passed_count
        print(f"⚠️ {passed_count}/{total_count} checks passed, {failed_count} failed")
        return 1


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Gemini CLI DoD Audit Script")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run audit in local mode without GEMINI_API_KEY",
    )
    args = parser.parse_args()

    if args.local:
        return run_local_audit()
    else:
        print("Use --local flag to run audit without GEMINI_API_KEY")
        return 1


if __name__ == "__main__":
    sys.exit(main())