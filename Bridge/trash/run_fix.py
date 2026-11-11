import os

os.chdir("C:/Users/crmte/OneDrive/Desktop/Projects/Discovery_Engine")

with open("05_Knowledge_Aggregator/intake_processor.py", "r") as f:
    content = f.read()

# Replace category loop
old = 'for category in ["raw_cognitive_models", "structural_analogies", "conceptual_schemes"]:'
new = 'for category in ["raw_cognitive_models", "structural_analogies", "conceptual_schemes", "image_metadata", "video_index"]:'
content = content.replace(old, new, 1)

# Replace report filename
old2 = 'report_name = f"report_intake_{timestamp}.md"'
new2 = 'report_name = f"report_rdf_cross_linking_{timestamp}.md"'
content = content.replace(old2, new2, 1)

with open("05_Knowledge_Aggregator/intake_processor.py", "w") as f:
    f.write(content)
print("Done modifying intake_processor.py")