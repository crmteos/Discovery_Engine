"""
Markdown State Decoder.
Translates formal Knowledge Graph triples and mathematical invariants into human-readable Markdown.
"""
from typing import List, Dict, Any

class MarkdownDecoder:
    def __init__(self, title: str = "Formal State Report"):
        self.title = title

    def decode_triples(self, triples: List[Dict[str, str]]) -> str:
        """Converts a list of RDF/KG triples into a structured Markdown list."""
        md = f"# {self.title}\n\n"
        md += "## Identified Formal Triples\n\n"
        for t in triples:
            sub = t.get("subject", "Unknown")
            pred = t.get("predicate", "relatedTo")
            obj = t.get("object", "Unknown")
            md += f"- **{sub}** `[{pred}]` ➔ **{obj}**\n"
        return md

    def decode_invariants(self, invariants: Dict[str, str]) -> str:
        """Decodes validated SymPy invariants into LaTeX Markdown blocks."""
        md = "## Validated Mathematical Invariants\n\n"
        for name, expr in invariants.items():
            md += f"### {name}\n"
            md += f"$$\n{expr}\n$$\n\n"
        return md

if __name__ == "__main__":
    decoder = MarkdownDecoder(title="Test State Projection")
    sample_triples = [{"subject": "Energy", "predicate": "equals", "object": "MassTimesSpeedOfLightSquared"}]
    sample_invariants = {"RelativisticEnergy": "E = m * c**2"}
    print(decoder.decode_triples(sample_triples))
    print(decoder.decode_invariants(sample_invariants))