#!/usr/bin/env python3
"""Integration tests for genkit_tracer.py"""
import py_compile
import sys
from pathlib import Path

PROJECT_ROOT = Path("C:/Users/crmte/OneDrive/Desktop/Projects/Discovery_Engine")
sys.path.insert(0, str(PROJECT_ROOT))
# Add project source to path
SRC_PATH = PROJECT_ROOT / "00_Project_Interface" / "src"
sys.path.insert(0, str(SRC_PATH))
from genkit_tracer import (
    trace_flow,
    get_traces,
    get_trace_stats,
    clear_traces,
    ensure_trace_dir,
)


def test_py_compile():
    """Validate that genkit_tracer.py passes py_compile check."""
    tracer_path = PROJECT_ROOT / "00_Project_Interface" / "src" / "genkit_tracer.py"
    print(f"Testing py_compile on: {tracer_path}")
    py_compile.compile(str(tracer_path), doraise=True)
    print(f"✅ py_compile PASSED: {tracer_path}")
    return True


def test_trace_flow_recording():
    """Test that trace_flow records entries correctly."""
    print("Testing trace_flow recording...")

    # Ensure trace directory exists
    ensure_trace_dir()

    # Clear any existing traces
    clear_traces()

    # Record a trace entry
    trace_flow(
        flow_name="test_extraction_flow",
        node="Node05",
        prompt="Extract entities from: The quick brown fox",
        input_data={"text": "The quick brown fox jumps over the lazy dog"},
        output_data={"entities": ["fox"], "count": 1},
        latency_ms=45.5,
        error=None,
    )

    # Verify trace was recorded
    traces = get_traces()
    assert len(traces) == 1, f"Expected 1 trace, got {len(traces)}"

    trace = traces[0]
    assert trace["flow_name"] == "test_extraction_flow", \
        f"Expected flow_name 'test_extraction_flow', got '{trace['flow_name']}'"
    assert trace["node"] == "Node05", \
        f"Expected node 'Node05', got '{trace['node']}'"
    assert trace["prompt"] == "Extract entities from: The quick brown fox", \
        f"Expected prompt, got '{trace['prompt']}'"
    assert trace["input_data"] == {"text": "The quick brown fox jumps over the lazy dog"}, \
        f"Expected input_data, got '{trace['input_data']}'"
    assert trace["output_data"] == {"entities": ["fox"], "count": 1}, \
        f"Expected output_data, got '{trace['output_data']}'"
    assert trace["latency_ms"] == 45.5, \
        f"Expected latency_ms 45.5, got '{trace['latency_ms']}'"
    assert trace["error"] is None, f"Expected error=None, got '{trace['error']}'"

    print("✅ trace_flow recording test PASSED")
    return True


def test_trace_stats():
    """Test that get_trace_stats returns correct statistics."""
    print("Testing get_trace_stats...")

    # Start with clean state for accurate stats
    clear_traces()

    stats = get_trace_stats()
    assert isinstance(stats, dict), f"Expected dict, got {type(stats)}"
    assert "total_traces" in stats, "Expected 'total_traces' in stats"
    assert "flows" in stats, "Expected 'flows' in stats"
    assert "nodes" in stats, "Expected 'nodes' in stats"

    print(f"✅ get_trace_stats test PASSED: {stats}")
    return True


def test_trace_filtering():
    """Test trace filtering by flow_name and node."""
    print("Testing trace filtering...")

    # Start with clean state for accurate filtering tests
    clear_traces()

    # Record traces for different nodes
    trace_flow(flow_name="flow_a", node="Node05", prompt="Prompt A")
    trace_flow(flow_name="flow_a", node="Node06", prompt="Prompt B")
    trace_flow(flow_name="flow_b", node="Node05", prompt="Prompt C")

    # Test flow_name filtering
    traces_a = get_traces(flow_name="flow_a")
    assert len(traces_a) == 2, f"Expected 2 traces for flow_a, got {len(traces_a)}"

    traces_b = get_traces(flow_name="flow_b")
    assert len(traces_b) == 1, f"Expected 1 trace for flow_b, got {len(traces_b)}"

    # Test node filtering
    traces_node05 = get_traces(node="Node05")
    assert len(traces_node05) == 2, f"Expected 2 traces for Node05, got {len(traces_node05)}"

    traces_node06 = get_traces(node="Node06")
    assert len(traces_node06) == 1, f"Expected 1 trace for Node06, got {len(traces_node06)}"

    print("✅ trace filtering test PASSED")
    return True


def test_clear_traces():
    """Test that clear_traces clears the log file."""
    print("Testing clear_traces...")

    # Start with clean state for this test
    clear_traces()

    # Record a trace
    trace_flow(flow_name="temp_flow", node="Node05", prompt="Temp prompt")

    # Verify it's there
    traces_before = get_traces()
    assert len(traces_before) == 1, f"Expected 1 trace before clear, got {len(traces_before)}"

    # Clear traces
    clear_traces()

    # Verify it's gone
    traces_after = get_traces()
    assert len(traces_after) == 0, f"Expected 0 traces after clear, got {len(traces_after)}"

    print("✅ clear_traces test PASSED")
    return True


def test_integration_run():
    """Full integration test: record traces, verify stats, then clear."""
    print("Running full integration test...")

    # Ensure directory exists
    ensure_trace_dir()

    # Clear starting state
    clear_traces()

    # Record multiple traces
    trace_flow(flow_name="integration_test", node="Node05",
               prompt="Test prompt 1", input_data={"a": 1}, output_data={"b": 2},
               latency_ms=10.0)
    trace_flow(flow_name="integration_test", node="Node06",
               prompt="Test prompt 2", input_data={"c": 3}, output_data={"d": 4},
               latency_ms=20.0)
    trace_flow(flow_name="other_flow", node="Node05",
               prompt="Test prompt 3", input_data={"e": 5}, output_data={"f": 6},
               latency_ms=30.0)

    # Check stats
    stats = get_trace_stats()
    assert stats["total_traces"] == 3, f"Expected 3 traces, got {stats['total_traces']}"
    assert "integration_test" in stats["flows"], "Expected 'integration_test' in flows"
    assert stats["flows"]["integration_test"] == 2, \
        f"Expected 2 integration_test flows, got {stats['flows'].get('integration_test')}"
    assert "Node05" in stats["nodes"], "Expected 'Node05' in nodes"
    assert stats["nodes"]["Node05"] == 2, \
        f"Expected 2 Node05 entries, got {stats['nodes'].get('Node05')}"

    # Filter by flow_name
    integration_traces = get_traces(flow_name="integration_test")
    assert len(integration_traces) == 2, \
        f"Expected 2 integration traces, got {len(integration_traces)}"

    # Filter by node
    node05_traces = get_traces(node="Node05")
    assert len(node05_traces) == 2, \
        f"Expected 2 Node05 traces, got {len(node05_traces)}"

    # Clear and verify
    clear_traces()
    stats_after = get_trace_stats()
    assert stats_after["total_traces"] == 0, \
        f"Expected 0 traces after clear, got {stats_after['total_traces']}"

    print("✅ Integration test PASSED")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Genkit Tracing Integration Tests")
    print("=" * 60)

    results = []

    # Test 1: py_compile
    print("\n[1/6] Testing py_compile...")
    try:
        results.append(("py_compile", test_py_compile()))
    except Exception as e:
        print(f"❌ py_compile FAILED: {e}")
        results.append(("py_compile", False))

    # Test 2: trace_flow recording
    print("\n[2/6] Testing trace_flow recording...")
    try:
        results.append(("trace_flow_recording", test_trace_flow_recording()))
    except Exception as e:
        print(f"❌ trace_flow_recording FAILED: {e}")
        results.append(("trace_flow_recording", False))

    # Test 3: trace_stats
    print("\n[3/6] Testing get_trace_stats...")
    try:
        results.append(("trace_stats", test_trace_stats()))
    except Exception as e:
        print(f"❌ trace_stats FAILED: {e}")
        results.append(("trace_stats", False))

    # Test 4: trace filtering
    print("\n[4/6] Testing trace filtering...")
    try:
        results.append(("trace_filtering", test_trace_filtering()))
    except Exception as e:
        print(f"❌ trace_filtering FAILED: {e}")
        results.append(("trace_filtering", False))

    # Test 5: clear_traces
    print("\n[5/6] Testing clear_traces...")
    try:
        results.append(("clear_traces", test_clear_traces()))
    except Exception as e:
        print(f"❌ clear_traces FAILED: {e}")
        results.append(("clear_traces", False))

    # Test 6: Integration run
    print("\n[6/6] Running integration test...")
    try:
        results.append(("integration_run", test_integration_run()))
    except Exception as e:
        print(f"❌ integration_run FAILED: {e}")
        results.append(("integration_run", False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

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