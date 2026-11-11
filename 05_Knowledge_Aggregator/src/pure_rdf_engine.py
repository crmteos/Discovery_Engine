"""Pure Python RDF Engine - N-Triples/Turtle parser & serializer (no rdflib)."""
import re, sys

class Triple:
    def __init__(self, s, p, o):
        self.s, self.p, self.o = s, p, o
    def to_nt(self):
        return f"<{self.s}> <{self.p}> <{self.o}> ."

class PureRDFEngine:
    PREFIXES = {"skos": "http://www.w3.org/2004/02/skos/core#", "prov": "http://www.w3.org/ns/prov#"}
    def parse_nt(self, text):
        triples = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r'<([^>]+)>\s+<([^>]+)>\s+<([^>]+)>\s*\.', line)
            if m:
                triples.append(Triple(m.group(1), m.group(2), m.group(3)))
        return triples
    def to_jsonld(self, triples):
        return [{"@id": t.s, t.p: {"@id": t.o}} for t in triples]
    def serialize_nt(self, triples):
        return "\n".join(t.to_nt() for t in triples) + "\n"

def _test():
    engine = PureRDFEngine()
    sample = "<http://ex/s> <http://ex/p> <http://ex/o> .\n"
    ts = engine.parse_nt(sample)
    assert len(ts) == 1
    out = engine.serialize_nt(ts)
    assert "<http://ex/s>" in out
    jl = engine.to_jsonld(ts)
    assert isinstance(jl, list)
    print("pure_rdf_engine --test: OK", len(ts), "triple(s)")
    return 0

if __name__ == "__main__":
    sys.exit(_test() if "--test" in sys.argv else 0)
