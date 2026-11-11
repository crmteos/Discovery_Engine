"""
Mathematical & Graph Visualizer.
Generates DOT representations for Knowledge Graphs and plot specifications for formal curves.
"""
from typing import List, Dict

class VisualDecoder:
    @staticmethod
    def generate_dot_graph(triples: List[Dict[str, str]]) -> str:
        """Generates a Graphviz DOT script from Knowledge Graph triples."""
        dot = "digraph FormalUniverse {\n"
        dot += "    rankdir=LR;\n"
        dot += '    node [shape=box, style="filled,rounded", fillcolor="#f0f4f8", fontname="Arial"];\n'
        dot += '    edge [fontname="Arial", fontsize=10];\n\n'
        
        for t in triples:
            sub = t.get("subject", "A").replace(" ", "_")
            pred = t.get("predicate", "relates").replace(" ", "_")
            obj = t.get("object", "B").replace(" ", "_")
            dot += f'    "{sub}" -> "{obj}" [label="{pred}"];\n'
        
        dot += "}\n"
        return dot

if __name__ == "__main__":
    sample_triples = [
        {"subject": "Entity_A", "predicate": "mapsTo", "object": "Entity_B"},
        {"subject": "Entity_B", "predicate": "preserves", "object": "Invariant_C"}
    ]
    print(VisualDecoder.generate_dot_graph(sample_triples))