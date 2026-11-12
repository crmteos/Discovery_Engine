#!/usr/bin/env python3
"""
start_genkit_ui.py - Genkit Developer UI Launcher Script

Command-line utility to invoke `npx genkit start` or launch the local trace viewer.
Includes --check-deps flag to verify local Node.js/npx availability without failing
build pipelines when absent.
"""

import subprocess
import sys
import argparse
from pathlib import Path


# Project root detection
PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENKIT_CMD = "npx genkit"


def check_deps() -> bool:
    """
    Check if Node.js and npx are available.

    Returns:
        True if dependencies are available, False otherwise.
    """
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            print("❌ Node.js not found. Please install Node.js.")
            return False

        print(f"✓ Node.js {result.stdout.strip()} found")

        result = subprocess.run(
            ["npx", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            print("❌ npx not found.")
            return False

        print(f"✓ npx {result.stdout.strip()} found")
        return True

    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js.")
        return False
    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False


def start_genkit() -> int:
    """
    Launch the Genkit Developer UI.

    Returns:
        Exit code from the genkit command.
    """
    print(f"🚀 Starting Genkit Developer UI...")
    print(f"Running: {GENKIT_CMD} start")

    try:
        result = subprocess.run(
            [GENKIT_CMD, "start"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        return result.returncode

    except subprocess.TimeoutExpired:
        print("⏱️ Genkit UI startup timed out after 60 seconds.")
        return 124
    except FileNotFoundError:
        print(f"❌ {GENKIT_CMD} not found. Make sure Node.js and npx are installed.")
        return 127
    except Exception as e:
        print(f"❌ Error starting Genkit UI: {e}")
        return 1


def launch_trace_viewer() -> int:
    """
    Launch the local Genkit trace viewer.

    Returns:
        Exit code from the command.
    """
    print("👀 Launching Genkit Trace Viewer...")

    # Try to launch the genkin trace viewer
    try:
        result = subprocess.run(
            [GENKIT_CMD, "visualize"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        return result.returncode

    except FileNotFoundError:
        print("ℹ️ No trace viewer command available. "
              "Use 'npx genkin start' for the full UI.")
        return 1
    except Exception as e:
        print(f"❌ Error launching trace viewer: {e}")
        return 1


def main() -> int:
    """
    Main entry point for start_genkit_ui.py.

    Parses arguments and executes the requested action.
    """
    parser = argparse.ArgumentParser(
        description="Genkit Developer UI Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check if Node.js/npx are available without failing build pipelines",
    )

    parser.add_argument(
        "--start",
        action="store_true",
        help="Launch the Genkit Developer UI (npx genkit start)",
    )

    parser.add_argument(
        "--trace",
        action="store_true",
        help="Launch the Genkin trace viewer",
    )

    args = parser.parse_args()

    # Handle --check-deps flag
    if args.check_deps:
        print("Checking Genkit UI dependencies...")
        if check_deps():
            print("\n✅ All dependencies are available.")
            return 0
        else:
            print("\�❌ Dependencies check failed.")
            return 1

    # If no specific flag, show help
    if not any([args.start, args.trace]):
        parser.print_help()
        return 0

    # Check dependencies if starting or tracing
    if args.start or args.trace:
        if not check_deps():
            return 1

    # Execute requested action
    if args.start:
        return start_genkit()

    if args.trace:
        return launch_trace_viewer()

    return 0


if __name__ == "__main__":
    sys.exit(main())