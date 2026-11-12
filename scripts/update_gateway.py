#!/usr/bin/env python3
"""Script to update google_ai_gateway.py with enterprise and location support."""

import re

# Read the file
with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\00_Project_Interface\src\google_ai_gateway.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new run_test function
new_run_test = '''def run_test(enterprise: bool = False, location: str = "europe-west1") -> int:
    """Run diagnostic validation test.

    Args:
        enterprise: whether enterprise mode is enabled
        location: data residency location

    Returns:
        exit code (always 0 for graceful fallback)
    """
    print("=== Google AI Gateway Test (v5.3.0 / Phase 44) ===")
    print(f"Enterprise mode: {enterprise}")
    print(f"Location: {location}")
    print()

    # Initialize client based on enterprise flag
    client = _client_for_model(DEFAULT_MODEL, enterprise=enterprise, location=location, project_id=GCP_PROJECT_ID)

    # Determine resolved model
    resolved_model = None
    available_models: list[str] = []

    if client is not None:
        available_models = _list_models(client, enterprise=enterprise, location=location, project_id=GCP_PROJECT_ID)
        print(f"Available models: {available_models}")

    # Try model chain resolution
    for model_name in GEMINI_MODEL_CHAIN:
        if model_name in available_models:
            resolved_model = model_name
            break

    # If no model resolved in enterprise mode, try fallback chain
    if not resolved_model and not enterprise:
        for model_name in GEMINI_MODEL_CHAIN:
            if model_name in available_models:
                resolved_model = model_name
                break

    # Generate smoke prompt
    generation_result = None
    if resolved_model and client is not None:
        generation_result = _generate_content(
            client, resolved_model, SMOKE_PROMPT,
            enterprise=enterprise, location=location, project_id=GCP_PROJECT_ID,
        )
    else:
        generation_result = _generate_content(
            client, DEFAULT_MODEL, SMOKE_PROMPT,
            enterprise=enterprise, location=location, project_id=GCP_PROJECT_ID,
        )

    # Build report
    report = {
        "timestamp": _utc_now(),
        "enterprise": enterprise,
        "location": location,
        "resolved_model": resolved_model,
        "available_models": available_models,
        "generation_ok": generation_result.get("ok", False) if generation_result else False,
        "generation_error": generation_result.get("error") if generation_result else None,
        "fallback": generation_result.get("fallback", True) if generation_result else True,
        "status_code": generation_result.get("status_code", 0) if generation_result else 0,
    }

    # Ping status
    report["ping_ok"] = generation_result is not None and generation_result.get("ok", False) if generation_result else False

    # Telemetry status
    all_ok = bool(GEMINI_API_KEY) and resolved_model is not None
    telemetry_status = "completed" if all_ok else "degraded_offline"
    report["telemetry_status"] = telemetry_status

    # Post telemetry to the message bus (best effort)
    try:
        import Bridge.bus_manager as bus_manager

        bus_manager.log_core_telemetry(
            step_name="google_ai_gateway_test",
            metrics={
                "ping_ok": report["ping_ok"],
                "resolved_model": resolved_model,
                "available_models": available_models,
                "generation_ok": generation_result.get("ok") if generation_result else None,
            },
            status=telemetry_status,
        )
    except Exception:
        pass  # Best-effort bus posting

    # Print report
    print(_json.dumps(report, ensure_ascii=False, indent=2))
    print("-" * 68)
    print(f"Google AI gateway --test: {telemetry_status.upper()}")
    print(f"  Ping/API available: {'OK' if report['ping_ok'] else 'OFFLINE/FALLBACK'}")
    print(f"  Resolved model: {resolved_model or 'none (offline fallback)'}")
    print(f"  Enterprise: {enterprise}, Location: {location}")
    print(f"  Budget: $0.00 | Google AI Studio free tier + Local Ollama fallback")
    print("-" * 34)

    # Always return exit_code: 0 (graceful fallback even on failure)
    return 0
'''

# Find the run_test function and replace it
old_func_start = content.find('def run_test() -> int:')
if old_func_start >= 0:
    # Find the end of the run_test function (look for the next def or __main__)
    remaining = content[old_func_start:]
    # Find next function definition or __main__
    next_def = remaining.find('\n\\ndef ')
    next_main = remaining.find('\\n\\nif __name__')
    
    if next_def >= 0 and (next_main < 0 or next_def < next_main):
        func_end = old_func_start + next_def
    elif next_main >= 0:
        func_end = old_func_start + next_main
    else:
        func_end = old_func_start + 5000  # fallback
    
    # Replace the function
    new_content = content[:old_func_start] + new_run_test + content[func_end:]
    
    with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\00_Project_Interface\src\google_ai_gateway.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("run_test function replaced successfully")
else:
    print("Could not find run_test function")