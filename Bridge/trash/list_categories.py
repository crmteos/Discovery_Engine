import os

intake_dir = "05_Knowledge_Aggregator/Intake_Queue"
categories = [d for d in os.listdir(intake_dir) 
              if os.path.isdir(os.path.join(intake_dir, d))]
print("Categories in Intake_Queue:")
for c in categories:
    print(f"  {c}")
    json_files = [f for f in os.listdir(os.path.join(intake_dir, c)) 
                  if f.endswith(".json")]
    print(f"    JSON files: {json_files}")