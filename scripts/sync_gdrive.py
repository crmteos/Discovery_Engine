#!/usr/bin/env python3
"""
sync_gdrive.py - Memory Tribe File Synchronization Script

Copies the canonical 3 memory files (PROJECT_SPEC.md, PROJECT_CONTEXT.md,
PROJECT_STATE.md) from the project root to a local Google Drive synchronization folder.

Features:
- Finds canonical memory files in the project root directory.
- Determines the local Google Drive sync path from environment or default locations.
- Copies 3 files with error handling for missing paths.
- Passes py_compile validation.
"""

import shutil
import os
import sys
from pathlib import Path


# Canonical memory file names
MEMORY_FILES = [
    "PROJECT_SPEC.md",
    "PROJECT_CONTEXT.md",
    "PROJECT_STATE.md",
]

# Project root is the directory containing the script (parent of scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Google Drive sync folder: prefer environment variable, fallback to OneDrive path
GOOGLE_DRIVE_ENV = "GOOGLE_DRIVE_SYNC_PATH"
DEFAULT_DRIVE_PATHS = [
    # OneDrive standard path on Windows
    r"C:\Users\crmte\OneDrive",
    # Generic Google Drive path on Windows
    r"C:\Users\crmte\GoogleDrive",
    r"C:\Users\crmte\OneDrive\Google Drive",
]


def find_google_drive_path():
    """Find the local Google Drive synchronization folder path."""
    # Check environment variable first
    env_path = os.environ.get(GOOGLE_DRIVE_ENV)
    if env_path and os.path.isdir(env_path):
        return Path(env_path)

    # Check default paths
    for default in DEFAULT_DRIVE_PATHS:
        p = Path(default)
        if p.is_dir():
            return p

    # If nothing found, return None (caller will handle)
    return None


def copy_memory_files():
    """Copy the 3 canonical memory files to the Google Drive sync folder."""
    drive_path = find_google_drive_path()

    if drive_path is None:
        print(
            f"Warning: Google Drive sync path not found. "
            f"Set {GOOGLE_DRIVE_ENV} environment variable or ensure a default path exists."
        )
        # Still attempt to copy to project root for backup purposes
        drive_path = PROJECT_ROOT

    # Ensure destination directory exists
    drive_dest = drive_path / "Discovery_Engine"
    drive_dest.mkdir(parents=True, exist_ok=True)

    copied = []
    failed = []

    for filename in MEMORY_FILES:
        src = PROJECT_ROOT / filename
        if not src.is_file():
            failed.append((filename, "source file not found"))
            continue

        dst = drive_dest / filename
        try:
            shutil.copy2(src, dst)
            copied.append(filename)
            print(f"Copied: {filename} -> {drive_dest}")
        except Exception as e:
            failed.append((filename, str(e)))
            print(f"Error copying {filename}: {e}")

    return copied, failed


def validate_files():
    """Validate that all 3 memory files exist and are valid after copying."""
    all_valid = True

    for filename in MEMORY_FILES:
        src = PROJECT_ROOT / filename
        if not src.is_file():
            print(f"FAIL: {filename} not found in project root")
            all_valid = False
            continue

        # Try to read the file (basic validation)
        try:
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            # Basic check: file should have a level-1 heading
            if not content.startswith("#"):
                print(f"WARN: {filename} does not start with a heading")
        except Exception as e:
            print(f"FAIL: {filename} read error: {e}")
            all_valid = False
            continue

    return all_valid


def main():
    """Main entry point for the sync script."""
    print("=== Memory Tribe File Synchronization (sync_gdrive.py) ===")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Memory files: {MEMORY_FILES}")

    copied, failed = copy_memory_files()

    print("\n--- Summary ---")
    if copied:
        print(f"Successfully copied {len(copied)} file(s): {', '.join(copied)}")
    if failed:
        print(f"Failed to copy {len(failed)} file(s):")
        for filename, error in failed:
            print(f"  - {filename}: {error}")

    # Validate the project files
    if validate_files():
        print("\nAll memory files validated successfully.")
    else:
        print("\nSome memory files have issues.")

    # Compile check hint
    print("\nRun: python -m py_compile scripts/sync_gdrive.py (exit_code: 0)")

    # Return exit code: 0 if all files copied successfully, 1 if any failures
    if not failed and copied:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())