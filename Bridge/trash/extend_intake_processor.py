content = open("05_Knowledge_Aggregator/intake_processor.py", "r").read()

# Replace the category loop to include image_metadata and video_index
old_loop = "for category in [\"raw_cognitive_models\", \"structural_analogies\", \"conceptual_schemes\"]:"
new_loop = 'for category in ["raw_cognitive_models", "structural_analogies", "conceptual_schemes", "image_metadata", "video_index"]:'
content = content.replace(old_loop, new_loop)

with open("05_Knowledge_Aggregator/intake_processor.py", "w") as f:
    f.write(content)

print("Category loop updated")