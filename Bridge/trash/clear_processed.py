import pathlib
p = pathlib.Path("05_Knowledge_Aggregator/Processed_Gate/normalized_triples")
for f in p.glob("*.json"):
    unlink(f)
print("Cleared normalized triples")