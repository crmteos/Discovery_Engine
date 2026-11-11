#!/usr/bin/env python3
def save_envelopes(video_results: list) -> list:
    """Save generated video_index JSON envelopes to Intake_Queue/media/videos/."""
    saved_paths = []

    for result in video_results:
        filepath = result["filepath"]
        envelope = result["envelope"]

        # Save the envelope as a JSON file alongside the media
        output_filename = f"{filepath.stem}_video_index.json"
        output_path = filepath.parent / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(envelope, f, indent=2, ensure_ascii=False)

        saved_paths.append(output_path)
        print(f"Saved video index envelope: {output_path}")

    return saved_paths


def main():
    """Main entry point for video extractor."""
    print("=" * 60)
    print("Video Extractor — 05_Knowledge_Aggregator")
    print("=" * 60)

    # Process video files
    video_results = process_video_files()

    # Save envelopes
    saved = save_envelopes(video_results)

    # Print summary
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("-" * 60)
    print(f"Timestamp: {timestamp}")
    print(f"Videos processed: {len(video_results)}")
    print(f"Envelopes saved: {len(saved)}")
    print("=" * 60)

    return 0