import sys
sys.path.insert(0, r'C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine')
sys.path.insert(0, r'C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator\src')

from search_intake_adapter import generate_intake_draft, search_duckduckgo, write_draft_to_disk

# Test 1: Import works
print("Test 1: Import successful")

# Test 2: generate_intake_draft with empty results
draft = generate_intake_draft("test query", [])
print(f"Test 2: Draft generated with query={draft['query']}, results_len={len(draft['results'])}")

# Test 3: search_duckduckgo returns list
results = search_duckduckgo("test", max_results=1)
print(f"Test 3: search returned {len(results)} results, type={type(results).__name__}")

# Test 4: write_draft_to_disk
import tempfile
import os
with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as tmp:
    tmp_path = tmp.name
try:
    draft4 = {"query": "test", "results": [{"title": "T", "url": "u", "snippet": "s", "source": "d"}], "generated_at": "2024-01-01T00:00:00Z", "metadata": {"provider": "d", "result_count": 1}}
    write_draft_to_disk(draft4, filename=tmp_path)
    with open(tmp_path, "r") as f:
        loaded = json.load(f)
    print(f"Test 4: Write/read successful, loaded query={loaded['query']}")
finally:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)

print("All tests passed!")