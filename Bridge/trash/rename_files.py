import os

# Rename sample.json to include category name for proper detection
image_old = "05_Knowledge_Aggregator/Intake_Queue/image_metadata/sample.json"
image_new = "05_Knowledge_Aggregator/Intake_Queue/image_metadata/image_metadata.json"
video_old = "05_Knowledge_Aggregator/Intake_Queue/video_index/sample.json"
video_new = "05_Knowledge_Aggregator/Intake_Queue/video_index/video_index.json"

os.rename(image_old, image_new)
os.rename(video_old, video_new)

print("Files renamed successfully")
print(f"image: {image_old} -> {image_new}")
print(f"video: {video_old} -> {video_new}")