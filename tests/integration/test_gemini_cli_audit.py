#!/usr/bin/env python3
"""tests/integration/test_gemini_cli_audit.py - Integration Tests for Gemini CLI Audit"""

import py_compile
import subprocess
import sys
from pathlib import Path


# Project root detection
PROJECT_ROOT = Path("C:/Users/crmte/OneDrive/Desktop/Projects/Discovery_Engine")

# Add project root to path for imports
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.gemini_cli_audit import (
    check_no_paid_dependencies,
    check_offline_fallbacks,
    check_prov_o_metadata,
    check_pure_python_fallbacks,
    run_local_audit,
)


def test_py_compile():
    """Validate that gemini_cli_audit.py passes py_compile check."""
    script_path = PROJECT_ROOT / "scripts" / "gemini_cli_audit.py"
    test_path = PROJECT_ROOT / "tests" / "integration" / "test_gemini_cli_audit.py"

    py_compile.compile(str(script_path), doraise=True)
    py_compile.compile(str(test_path), doraise=True)

    print(f"✅ py_compile PASSED: {script_path}")
    print(f"✅ py_compile PASSED: {test_path}")
    return True


def test_local_audit_runs():
    """Test that the local audit runs without crashing."""
    print("Testing local audit execution...")

    result = subprocess.run(
        [sys.executable, "scripts/gemini_cli_audit.py", "--local"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )

    # The audit should exit with code 0 or a reasonable code
    # It must not crash (exit_code not due to error)
    assert result.returncode in [0, 1], (
        f"Audit crashed with unexpected exit code: {result.returncode}"
    )

    print(f"✅ Local audit execution PASSED (exit_code: {result.returncode})")
    return True


def test_audit_checks_exist():
    """Test that all audit check functions exist and are callable."""
    print("Testing audit check functions exist...")

    # Import functions and verify they're callable
    checks = [
        "check_no_paid_dependencies",
        "check_offline_fallbacks",
        "check_prov_o_metadata",
        "check_pure_python_fallbacks",
        "run_local_audit",
    ]

    for check_name in checks:
        # Verify function exists and is callable
        func = globals().get(check_name)
        if func is None:
            # Try importing from the module
            import importlib
            module = importlib.import_module("scripts.gemini_cli_audit")
            func = getattr(module, check_name, None)
        
        assert func is not None and callable(func), f"Missing check function: {check_name}"

    print(f"✅ All {len(checks)} audit check functions exist and are callable")
    return True


def test_no_critical_issues():
    """Test that critical issues are detected (or not, depending on codebase state)."""
    # This test verifies the audit can identify issues
    # It should not crash and should produce a result

    # Run check_no_paid_dependencies
    issues = check_no_paid_dependencies()
    assert isinstance(issues, list), "check_no_paid_dependencies should return a list"

    # Run check_offline_fallbacks
    issues_of = check_offline_fallbacks()
    assert isinstance(issues_of, list), "check_offline_fallbacks should return a list"

    # Run check_prov_o_metadata
    issues_pov = check_prov_o_metadata()
    assert isinstance(issues_pov, list), "check_prov_o_metadata should return a list"

    # Run check_pure_python_fallbacks
    issues_ppf = check_pure_python_fallbacks()
    assert isinstance(issues_ppf, list), "check_pure_python_fallbacks should return a list"

    print("✅ All audit checks return proper list types")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Gemini CLI Audit Integration Tests")
    print("=" * 60)

    results = []

    # Test 1: py_compile
    print("\n[1/5] Testing py_compile...")
    try:
        results.append(("py_compile", test_py_compile()))
    except Exception as e:
        print(f"❌ py_compile FAILED: {e}")
        results.append(("py_compile", False))

    # Test 2: local audit runs
    print("\n[2/5] Testing local audit runs...")
    try:
        results.append(("local_audit", test_local_audit_runs()))
    except Exception as e:
        print(f"❌ local_audit FAILED: {e}")
        results.append(("local_audit", False))

    # Test 3: audit checks exist
    print("\n[3/5] Testing audit checks exist...")
    try:
        results.append(("checks_exist", test_audit_checks_exist()))
    except Exception as e:
        print(f"❌ checks_exist FAILED: {e}")
        results.append(("checks_exist", False))

    # Test 4: no critical issues test
    print("\n[4/5] Testing no critical issues...")
    try:
        results.append(("no_critical", test_no_critical_issues()))
    except Exception as e:
        print(f"❌ no_critical FAILED: {e}")
        results.append(("no_critical", False))

    # Test 5: Summary
    print("\n[5/5] Summary...")
    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"  {name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)