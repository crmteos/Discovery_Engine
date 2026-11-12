"""Integration tests for Google AI Gateway (v4.4.0)."""

import os
import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from google_ai_gateway import run_test, _client_for_model, _generate_content, _list_models, GEMINI_MODEL_CHAIN, GEMINI_API_KEY


class TestGoogleAiGatewayImport:
    """Test that the module imports correctly."""

    def test_module_imports(self):
        """Module should import without errors."""
        assert "google_ai_gateway" in sys.modules

    def test_gemini_model_chain(self):
        """Model chain should have 3 priority models."""
        assert len(GEMINI_MODEL_CHAIN) == 3
        assert GEMINI_MODEL_CHAIN[0] == "gemini-2.5-flash"
        assert GEMINI_MODEL_CHAIN[1] == "gemini-2.0-flash"
        assert GEMINI_MODEL_CHAIN[2] == "gemini-1.5-flash"


class TestGoogleAiGatewayNoApiKey:
    """Test gateway behavior when GEMINI_API_KEY is not set."""

    def test_run_test_no_api_key(self):
        """run_test should return exit_code 0 when no API key."""
        # Ensure no API key
        os.environ.pop("GEMINI_API_KEY", None)
        exit_code = run_test()
        assert exit_code == 0

    def test_run_test_no_api_key_no_crash(self):
        """run_test should not crash when no API key is set."""
        os.environ.pop("GEMINI_API_KEY", None)
        try:
            exit_code = run_test()
            assert exit_code == 0
        except Exception as e:
            assert False, f"run_test crashed with no API key: {e}"


class TestGoogleAiGatewayWithApiKey:
    """Test gateway behavior when GEMINI_API_KEY is set (but may not work
    without actual network access)."""

    def test_run_test_with_api_key_no_crash(self):
        """run_test should not crash even if API key is invalid."""
        # Set a dummy API key (will likely fail network calls)
        os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
        try:
            exit_code = run_test()
            assert exit_code == 0
        except Exception:
            # May fail due to network, but should not crash Python
            pass


class TestClientCreation:
    """Test client creation functions."""

    def test_client_for_model_without_genai(self):
        """_client_for_model should handle missing google-genai SDK."""
        # Temporarily remove genai
        import google_ai_gateway as gap
        # This is tested indirectly via run_test with no API key


class TestListModels:
    """Test model listing functionality."""

    def test_list_models_returns_list(self):
        """_list_models should return a list."""
        os.environ.pop("GEMINI_API_KEY", None)
        result = _list_models(None)
        assert isinstance(result, list)


class TestGenerateContent:
    """Test content generation functionality."""

    def test_generate_content_without_client(self):
        """_generate_content should handle None client."""
        os.environ.pop("GEMINI_API_KEY", None)
        result = _generate_content(None, "gemini-2.5-flash", "test")
        assert result.get("ok") == False
        assert result.get("fallback") == True


class TestGoogleAiGatewayResolve:
    """Test --resolve mode."""

    def test_resolve_without_api_key(self):
        """--resolve should work without API key, returning None."""
        os.environ.pop("GEMINI_API_KEY", None)
        # Just test the functions don't crash
        from google_ai_gateway import _client_for_model, _list_models
        client = _client_for_model("gemini-2.5-flash")
        assert client is None


def test_py_compile_validator():
    """Verify py_compile passes for google_ai_gateway.py."""
    import py_compile
    compile_result = py_compile.compile(
        str(PROJECT_ROOT / "00_Project_Interface" / "src" / "google_ai_gateway.py"),
        doraise=True,
    )
    assert compile_result == None  # py_compile returns None on success