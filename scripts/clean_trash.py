#!/usr/bin/env python3
"""Operational utility to manage/purge Bridge/trash/ directory."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRASH = ROOT / "Bridge" / "trash"

def main():
    parser = argparse.ArgumentParser(description="Manage Bridge/trash/")
    parser.add_argument("--list", action="store_true", help="List trash contents")
    parser.add_argument("--purge", action="store_true", help="Purge all trash contents")
    args = parser.parse_args()
    if not TRASH.exists():
        TRASH.mkdir(parents=True, exist_ok=True)
    if args.list:
        for p in TRASH.iterdir():
            print(p.name)
        return 0
    if args.purge:
        for p in TRASH.iterdir():
            if p.is_dir() and not p.is_symlink():
                shutil.rmtree(p)
            else:
                p.unlink()
        print("Trash purged.")
        return 0
    parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())