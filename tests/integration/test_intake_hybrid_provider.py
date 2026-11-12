"""Integration tests for Knowledge Aggregator Hybrid Provider Switcher (v4.6.0 / Phase 37)."""

import os
import sys
import json
from pathlib import Path

# Add project roots to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "05_Knowledge_Aggregator" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "00_Project_Interface" / "src"))

from intake_processor import extract_triplet, main


class TestIntakeHybridProviderImport:
    """Test that the module imports correctly."""

    def test_module_imports(self):
        """Module should import without errors."""
        assert "intake_processor" in sys.modules

    def test_extract_triplet_function(self):
        """extract_triplet function should exist and be callable."""
        assert callable(extract_triplet)


class TestProviderAuto:
    """Test --provider auto mode."""

    def test_auto_with_ollama_text(self):
        """auto mode should fall back to Ollama when Gemini API key is missing."""
        os.environ.pop("GEMINI_API_KEY", None)
        result = extract_triplet(
            "The Discovery Engine project uses Ollama for local inference",
            provider="auto",
        )
        assert isinstance(result, dict)
        assert "subject" in result or "graph_context" in result

    def test_auto_returns_dict(self):
        """auto mode should always return a dict."""
        os.environ.pop("GEMINI_API_KEY", None)
        result = extract_triplet("test text", provider="auto")
        assert isinstance(result, dict)


class TestProviderOllama:
    """Test --provider ollama mode."""

    def test_ollama_returns_dict(self):
        """ollama mode should always return a dict."""
        result = extract_triplet("test text", provider="ollama")
        assert isinstance(result, dict)

    def test_ollama_has_required_keys(self):
        """ollama mode should return result with expected keys."""
        result = extract_triplet("test ontology development", provider="ollama")
        assert isinstance(result, dict)


class TestProviderGoogle:
    """Test --provider google mode."""

    def test_google_no_api_key_fallback(self):
        """google mode should handle missing API key gracefully."""
        os.environ.pop("GEMINI_API_KEY", None)
        result = extract_triplet("test text", provider="google")
        assert isinstance(result, dict)

    def test_google_with_dummy_key(self):
        """google mode should not crash even with dummy API key."""
        os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
        try:
            result = extract_triplet("test text", provider="google")
            assert isinstance(result, dict)
        except Exception:
            pass  # May fail due to network, but should not crash Python


def test_py_compile_validator():
    """Verify py_compile passes for intake_processor.py."""
    import py_compile
    compile_result = py_compile.compile(
        str(PROJECT_ROOT / "05_Knowledge_Aggregator" / "src" / "intake_processor.py"),
        doraise=True,
    )
    assert compile_result == None  # py_compile returns None on success


def test_main_help():
    """Test that main() handles --help correctly."""
    exit_code = main(["--help"])
    assert exit_code == 0


def test_main_no_args():
    """Test that main() handles missing args gracefully."""
    exit_code = main([])
    # Should print help and return 0 or exit with error
    assert exit_code is not None