import os
os.chdir(r"C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine")

# Read current intake_processor.py
with open("05_Knowledge_Aggregator/intake_processor.py", "r") as f:
    content = f.read()

# Add validators if not present
validators_marker = "def _validate_cognitive_model(data):"
if validators_marker in content:
    # Add image/video validators after the last validator
    last_validator_pos = content.rfind("def _validate_concept_scheme")
    if last_validator_pos != -1:
        after_validator = content[last_validator_pos + len("def _validate_concept_scheme(data):\n    errors = []\n")]
        new_validators = '''

def _validate_image_metadata(data):
    errors = []
    for key in ["image_id", "source_path_or_url", "extracted_concepts", "prov", "confidence_score"]:
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if "prov" in data:
        prov = data["prov"]
        for pf in ["wasAttributedTo", "generatedAtTime", "hadPrimarySource"]:
            if pf not in prov:
                errors.append(f"prov missing required field: {pf}")
    if "skos" in data:
        skos = data["skos"]
        for sf in ["broader", "narrower", "related"]:
            if sf not in skos:
                errors.append(f"skos missing required field: {sf}")
    return errors


def _validate_video_index(data):
    errors = []
    for key in ["video_id", "source_path_or_url", "temporal_chunks", "prov", "confidence_score"]:
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if "prov" in data:
        prov = data["prov"]
        for pf in ["wasAttributedTo", "generatedAtTime", "hadPrimarySource"]:
            if pf not in prov:
                errors.append(f"prov missing required field: {pf}")
    if "skos" in data:
        skos = data["skos"]
        for sf in ["broader", "narrower", "related"]:
            if sf not in skos:
                errors.append(f"skos missing required field: {sf}")
    return errors
'''
        content = content[:last_validator_pos + len("def _validate_concept_scheme(data):\n    errors = []\n")] + new_validators + content[last_validator_pos + len("def _validate_concept_scheme(data):\n    errors = []\n"):]
        with open("05_Knowledge_Aggregator/intake_processor.py", "w") as f:
            f.write(content)
        print("Validators added")
    else:
        print("Could not find concept scheme validator position")
else:
    print("Already has validators marker")