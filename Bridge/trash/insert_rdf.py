import sys

with open("05_Knowledge_Aggregator/intake_processor.py", "r") as f:
    content = f.read()

rdf_functions = '''

def _generate_rdf_triples_from_cognitive_model(data, source_path):
    """Generate RDF N-Triples for a cognitive model with PROV-O and SKOS relationships."""
    triples = []
    model_id = data.get("metadata", {}).get("model_name", "unknown_model")
    attribution = data.get("prov", {}).get("wasAttributedTo", "aggregator.architect")
    timestamp = data.get("prov", {}).get("generatedAtTime", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    primary_source = data.get("prov", {}).get("hadPrimarySource", source_path)
    entities = data.get("entities", [])
    for ent in entities:
        ent_id = ent.get("id", "unknown")
        ent_name = ent.get("name", "unknown")
        ent_type = ent.get("type", "Concept")
        triples.append(f"<{ent_id}> rdf:type <{ent_type}> .")
        if "properties" in ent and "domain" in ent["properties"]:
            triples.append(f"<{ent_id}> skos:prefLabel \"{ent_name}\" .")
        triples.append(f"<{ent_id}> prov:wasAttributedTo <{attribution}> .")
    relations = data.get("relations", [])
    for rel in relations:
        sub = rel.get("subject", "unknown")
        pred = rel.get("predicate", "relatedTo")
        obj = rel.get("object", "unknown")
        triples.append(f"<{sub}> <{pred}> <{obj}> .")
    triples.append(f"<{model_id}> prov:wasAttributedTo <{attribution}> .")
    triples.append(f"<{model_id}> prov:generatedAtTime \"{timestamp}\"^^xsd:dateTime .")
    triples.append(f"<{model_id}> prov:hadPrimarySource <{primary_source}> .")
    return triples

def _generate_rdf_triples_from_image_metadata(data, source_path):
    """Generate RDF N-Triples for image metadata with PROV-O and SKOS relationships."""
    triples = []
    image_id = data.get("image_id", "unknown_image")
    attribution = data.get("prov", {}).get("wasAttributedTo", "aggregator.architect")
    timestamp = data.get("prov", {}).get("generatedAtTime", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    primary_source = data.get("prov", {}).get("hadPrimarySource", source_path)
    extracted_concepts = data.get("extracted_concepts", [])
    for concept in extracted_concepts:
        concept_name = concept.get("concept_name", "unknown")
        definition = concept.get("definition", "")
        triples.append(f"<{image_id}> skos:related <{concept_name}> .")
        if definition:
            triples.append(f"<{concept_name}> skos:definition \"{definition}\" .")
        triples.append(f"<{concept_name}> prov:wasAttributedTo <{attribution}> .")
    triples.append(f"<{image_id}> prov:wasAttributedTo <{attribution}> .")
    triples.append(f"<{image_id}> prov:generatedAtTime \"{timestamp}\"^^xsd:dateTime .")
    triples.append(f"<{image_id}> prov:hadPrimarySource <{primary_source}> .")
    visual_keys = data.get("visual_keys", [])
    for i, key in enumerate(visual_keys):
        triples.append(f"<{image_id}> skos:related \"{key}\" .")
    return triples

def _generate_rdf_triples_from_video_index(data, source_path):
    """Generate RDF N-Triples for video index with PROV-O and SKOS relationships."""
    triples = []
    video_id = data.get("video_id", "unknown_video")
    attribution = data.get("prov", {}).get("wasAttributedTo", "aggregator.architect")
    timestamp = data.get("prov", {}).get("generatedAtTime", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    primary_source = data.get("prov", {}).get("hadPrimarySource", source_path)
    temporal_chunks = data.get("temporal_chunks", [])
    for chunk in temporal_chunks:
        chunk_id = chunk.get("chunk_id", "unknown_chunk")
        start_time = chunk.get("timestamp_start", "00:00:00")
        end_time = chunk.get("timestamp_end", "00:00:00")
        extracted_entities = chunk.get("extracted_entities", [])
        visual_keys = chunk.get("visual_keys", [])
        triples.append(f"<{chunk_id}> prov:wasAttributedTo <{attribution}> .")
        triples.append(f"<{chunk_id}> prov:generatedAtTime \"{timestamp}\"^^xsd:dateTime .")
        triples.append(f"<{chunk_id}> prov:hadPrimarySource <{primary_source}> .")
        triples.append(f"<{chunk_id}> skos:prefLabel \"{chunk_id} [{start_time}-{end_time}]\" .")
        for entity in extracted_entities:
            triples.append(f"<{chunk_id}> skos:related <{entity}> .")
        for i, key in enumerate(visual_keys):
            triples.append(f"<{chunk_id}> skos:related \"{key}\" .")
    triples.append(f"<{video_id}> prov:wasAttributedTo <{attribution}> .")
    triples.append(f"<{video_id}> prov:generatedAtTime \"{timestamp}\"^^xsd:dateTime .")
    triples.append(f"<{video_id}> prov:hadPrimarySource <{primary_source}> .")
    return triples

'''

# Find CONCEPT_REQUIRED_KEYS line and insert after it
marker = 'CONCEPT_REQUIRED_KEYS = ["name", "definition"]'
if marker in content:
    content = content.replace(marker, marker + rdf_functions)
    print("Inserted RDF functions after CONCEPT_REQUIRED_KEYS")
else:
    print("Marker not found!")

with open("05_Knowledge_Aggregator/intake_processor.py", "w") as f:
    f.write(content)
print("Done")