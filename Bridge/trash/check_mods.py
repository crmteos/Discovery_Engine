content = open("05_Knowledge_Aggregator/intake_processor.py").read()
# Check if modifications were applied
if 'for category in ["raw_cognitive_models", "structural_analogies", "conceptual_schemes", "image_metadata", "video_index"]:' in content:
    print("Category loop MODIFIED ✓")
else:
    print("Category loop NOT modified")
    
if 'report_rdf_cross_linking' in content:
    print("Report filename MODIFIED ✓") 
else:
    print("Report filename NOT modified")