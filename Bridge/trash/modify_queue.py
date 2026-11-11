import sys

with open("05_Knowledge_Aggregator/intake_processor.py", "r") as f:
    content = f.read()

# Find and replace the process_intake_queue function
# The old function processes only 3 categories; we need to add image_metadata and video_index

old_loop = 'for category in [\"raw_cognitive_models\", \"structural_analogies\", \"conceptual_schemes\"]:'
new_loop = 'for category in [\"raw_cognitive_models\", \"structural_analogies\", \"conceptual_schemes\", \"image_metadata\", \"video_index\"]:'
content = content.replace(old_loop, new_loop)
print("Updated category loop")

# Also need to update the report to reflect the new categories
old_report = 'report_intake_{timestamp}.md'
new_report = 'report_rdf_cross_linking_{timestamp}.md'
content = content.replace(old_report, new_report)
print("Updated report filename")

with open("05_Knowledge_Aggregator/intake_processor.py", "w") as f:
    f.write(content)
print("Done")