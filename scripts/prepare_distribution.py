"""
Script to prepare the distribution package for rFactor Championship Creator.

This script copies the compiled executable and necessary files to a distribution folder.
"""

import shutil
from pathlib import Path

# Project root
project_root = Path(__file__).parent.parent
dist_source = project_root / "dist" / "rfactor_championship_creator"
dist_target = project_root / "dist" / "rfactor_championship_creator_v1.3.0"

# Files to copy
files_to_copy = [
    "RUN_APP.bat",
    "README.md",
    "INSTALL.md",
    "config.json",
]

def prepare_distribution():
    """Prepare the distribution package."""
    print("=" * 70)
    print("    Preparing rFactor Championship Creator Distribution")
    print("=" * 70)
    print()

    # Check if source exists
    if not dist_source.exists():
        print(f"❌ ERROR: Source directory not found: {dist_source}")
        print("Please run PyInstaller first to build the executable.")
        return False

    # Create target directory if it doesn't exist
    print(f"Creating distribution directory: {dist_target}")
    dist_target.mkdir(parents=True, exist_ok=True)

    # Copy the entire build
    print(f"\nCopying executable and dependencies...")

    # Copy all files from source
    for item in dist_source.iterdir():
        target_path = dist_target / item.name
        if item.is_file():
            print(f"  Copying {item.name}...")
            shutil.copy2(item, target_path)
        elif item.is_dir():
            print(f"  Copying directory {item.name}...")
            if target_path.exists():
                shutil.rmtree(target_path)
            shutil.copytree(item, target_path)

    # Copy additional files from project root
    print("\nCopying additional files...")
    for filename in files_to_copy:
        source_file = project_root / filename
        if source_file.exists():
            print(f"  Copying {filename}...")
            shutil.copy2(source_file, dist_target / filename)
        else:
            print(f"  WARNING: {filename} not found, skipping")

    # Create empty logs directory
    logs_dir = dist_target / "logs"
    logs_dir.mkdir(exist_ok=True)
    print(f"\nCreated logs directory: {logs_dir}")

    print()
    print("=" * 70)
    print("    Distribution package ready!")
    print("=" * 70)
    print()
    print(f"Package location: {dist_target}")
    print()
    print("You can now distribute the contents of this folder.")
    print()

    return True


if __name__ == "__main__":
    success = prepare_distribution()
    if not success:
        exit(1)
