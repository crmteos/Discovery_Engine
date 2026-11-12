#!/usr/bin/env python3
"""Update PROJECT_CONTEXT.md with Vertex AI / Data Residency configuration."""

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\PROJECT_CONTEXT.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Vertex AI / Data Residency section after the Context Caching section
# Find the Context Caching section end and add new section
old_context_end = '''| Context Caching | Gemini Context Caching feature for specification documents (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`) with TTL management (5 min – 1 hr), reducing input token consumption by ~90% during multi-turn sessions |\n\nTelemetry from each `--test` run is posted to the Universal Message Bus (`Bridge/messages.jsonl`) via `Bridge/bus_manager.py` (`log_core_telemetry`).'''

new_context_end = '''| Context Caching | Gemini Context Caching feature for specification documents (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`) with TTL management (5 min – 1 hr), reducing input token consumption by ~90% during multi-turn sessions |\n\n| Vertex AI | Vertex AI Enterprise Agent Platform integration with data residency support |\n|-----------|-----------------------------------------------------------------------|\n| EU Region | `europe-west1` - European Union data residency |\n| US Region | `us-central1` - United States data residency |\n| Enterprise Mode | Controlled via `--enterprise` flag and `VERTEX_AI_ENABLED` environment variable |\n| GCP Project ID | Required for Vertex AI authorization via `GCP_PROJECT_ID` env var |\n\nTelemetry from each `--test` run is posted to the Universal Message Bus (`Bridge/messages.jsonl`) via `Bridge/bus_manager.py` (`log_core_telemetry`).'''

content = content.replace(old_context_end, new_context_end)

# Also update the budget and version info
content = content.replace('**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack)', '**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack - Enterprise Switcher enabled via Vertex AI)')

# Update the version reference
content = content.replace('v5.2.0 / Phase 43', 'v5.3.0 / Phase 44')

# Update the DoD reference
content = content.replace('Synchronized to `v5.2.0 / Phase 43` memory triad.', 'Synchronized to `v5.3.0 / Phase 44` memory triad.')

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\PROJECT_CONTEXT.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('PROJECT_CONTEXT.md updated successfully')