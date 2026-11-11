import sys
sys.path.insert(0, r'C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine')
sys.path.insert(0, r'C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator\src')

import search_intake_adapter as sia

print("Module loaded successfully")
print("DUCKDUCKGO_BASE_URL:", hasattr(sia, 'DUCKDUCKGO_BASE_URL'))
print("logger:", hasattr(sia, 'logger'))
print("REQUEST_TIMEOUT:", hasattr(sia, 'REQUEST_TIMEOUT'))

# Try calling search_duckduckgo
try:
    results = sia.search_duckduckgo("test", max_results=1)
    print("search_duckduckgo result:", len(results), "results")
except Exception as e:
    print("Error calling search_duckduckgo:", type(e).__name__, str(e))

# Try generate_intake_draft
try:
    draft = sia.generate_intake_draft("test query", [])
    print("generate_intake_draft OK, results_len:", len(draft['results']))
except Exception as e:
    print("Error calling generate_intake_draft:", type(e).__name__, str(e))