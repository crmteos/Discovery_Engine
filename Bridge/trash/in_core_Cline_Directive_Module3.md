# TASK DIRECTIVE: Module 3 Implementation — Multimodal State Decoders & Interfaces

**Target Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\03_Multimodal_Interface`
**Assigned Role:** Multimodal & Visual Decoder Engineer
**Sender:** Gemini Notebook (Architecture Lead)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Goal:** Implement multimodal decoders translating formal mathematical core states and Knowledge Graphs into human-readable text, math visualization specs (Graphviz/Matplotlib), and media rendering stubs.

---

## 1. Context Synchronization
Before executing, read `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\PROJECT_STATE.md` and check `03_Multimodal_Interface\INSTRUCTIONS_ROLE.md`.

---

## 2. File Implementation Tasks

### A. Text & Markdown State Decoder
**File Path:** `03_Multimodal_Interface/Decoders_Text/markdown_decoder.py`
Create a Python module that takes RDF triples or Knowledge Graph states and projects them into clean, structured Markdown reports.

```python
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
```

### B. Mathematical Visualizer (Graphviz / Matplotlib Spec Generator)
**File Path:** `03_Multimodal_Interface/Decoders_Visual/math_visualizer.py`
Create a visual decoder that generates Graphviz DOT specs and Matplotlib plot code directly from formal core structures.

```python
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
```

### C. Audio/Video Media Pipeline Interface Stub
**File Path:** `03_Multimodal_Interface/Decoders_Audio_Video/media_pipeline_stub.py`
Create a stub interface for future automated Manim/ffmpeg video generation and TTS audio narration pipelines.

```python
"""
Media Pipeline Interface Stub for Audio/Video Synthesis.
"""
from typing import Dict, Any

class MediaPipelineStub:
    def __init__(self, output_dir: str = "./media_output"):
        self.output_dir = output_dir

    def render_animation_spec(self, scene_name: str, parameters: Dict[str, Any]) -> Dict[str, str]:
        """Stub for compiling Manim animation scripts from formal equations."""
        return {
            "status": "queued",
            "scene": scene_name,
            "engine": "Manim",
            "output_path": f"{self.output_dir}/{scene_name}.mp4"
        }

    def render_narration_script(self, text_script: str) -> Dict[str, str]:
        """Stub for TTS audio rendering."""
        return {
            "status": "queued",
            "audio_engine": "TTS_Local",
            "output_path": f"{self.output_dir}/narration.wav"
        }

if __name__ == "__main__":
    pipeline = MediaPipelineStub()
    print(pipeline.render_animation_spec("InvariantTransformationScene", {"fps": 60}))
```

---

## 3. Project State Update & Reporting

Upon completing creation and syntax checks for all 3 files:
1. Update `PROJECT_STATE.md`:
   - Change `Module 3: Multimodal Interface` status to `Active`.
   - Log completed components (`markdown_decoder.py`, `math_visualizer.py`, `media_pipeline_stub.py`).
2. Save execution report to `Bridge/out/execution_reports/report_module3_[TIMESTAMP].md`.
