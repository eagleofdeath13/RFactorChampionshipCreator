"""
Configuration setup script for rFactor Championship Creator.

This script helps configure the application by:
1. Detecting or asking for rFactor installation path
2. Validating the installation
3. Selecting a player profile
4. Saving the configuration
"""

import sys
from pathlib import Path

from src.utils.config import Config
from src.utils.rfactor_validator import RFactorValidator, RFactorValidationError


def print_header(text: str):
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)
    print()


def print_section(text: str):
    """Print a formatted section header."""
    print()
    print("-" * 40)
    print(text)
    print("-" * 40)


def detect_rfactor_path() -> list:
    """
    Try to detect rFactor installation in common locations.

    Returns:
        List of potential rFactor paths
    """
    potential_paths = []

    # Common installation locations
    common_locations = [
        Path("C:/Program Files (x86)/rFactor"),
        Path("C:/Program Files/rFactor"),
        Path("D:/Games/rFactor"),
        Path("C:/Games/rFactor"),
        Path.home() / "Games" / "rFactor",
        # Steam locations
        Path("C:/Program Files (x86)/Steam/steamapps/common/rFactor"),
        Path("C:/Program Files/Steam/steamapps/common/rFactor"),
    ]

    for path in common_locations:
        if path.exists():
            is_valid, _ = RFactorValidator.validate(str(path))
            if is_valid:
                potential_paths.append(path)

    return potential_paths


def validate_and_show_info(path: str) -> bool:
    """
    Validate path and show info about the installation.

    Args:
        path: Path to validate

    Returns:
        True if valid, False otherwise
    """
    print(f"Validating: {path}")

    is_valid, missing = RFactorValidator.validate(path)

    if not is_valid:
        print("[ERROR] Invalid rFactor installation!")
        print(f"Missing items: {', '.join(missing)}")
        return False

    print("[OK] Valid rFactor installation found!")

    # Show info
    info = RFactorValidator.get_version_info(path)
    print()
    print("Installation details:")
    print(f"  - Talents available: {info.get('talent_count', 0)}")
    print(f"  - Vehicles available: {info.get('vehicle_count', 0)}")
    print(f"  - Locations available: {info.get('location_count', 0)}")

    return True


def select_player_profile(rfactor_path: str) -> str:
    """
    Let user select a player profile.

    Args:
        rfactor_path: Path to rFactor installation

    Returns:
        Selected player name
    """
    print_section("Player Profile Selection")

    players = RFactorValidator.list_player_profiles(rfactor_path)

    if not players:
        print("No player profiles found in UserData.")
        player_name = input("Enter player name to use: ").strip()
        return player_name

    print(f"Found {len(players)} player profile(s):")
    for i, player in enumerate(players, 1):
        print(f"  {i}. {player}")

    while True:
        choice = input("\nSelect player profile number (or enter new name): ").strip()

        # Check if it's a number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(players):
                return players[idx]
            else:
                print(f"[ERROR] Invalid number. Please enter 1-{len(players)}")
        else:
            # Use as new player name
            if choice:
                return choice
            print("[ERROR] Please enter a valid choice")


def main():
    """Main setup function."""
    print_header("rFactor Championship Creator - Configuration Setup")

    config = Config()

    # Check if already configured
    if config.is_configured():
        print("[INFO] Configuration already exists!")
        current_path = config.get_rfactor_path()
        current_player = config.get_current_player()
        print(f"  rFactor path: {current_path}")
        print(f"  Current player: {current_player}")
        print()

        reconfigure = input("Do you want to reconfigure? (y/n): ").strip().lower()
        if reconfigure != 'y':
            print("Configuration unchanged. Exiting.")
            return

    # Try to detect rFactor
    print_section("Detecting rFactor Installation")

    detected_paths = detect_rfactor_path()

    rfactor_path = None

    if detected_paths:
        print(f"Found {len(detected_paths)} potential rFactor installation(s):")
        for i, path in enumerate(detected_paths, 1):
            print(f"  {i}. {path}")
        print(f"  {len(detected_paths) + 1}. Enter custom path")

        while True:
            choice = input(f"\nSelect installation (1-{len(detected_paths) + 1}): ").strip()

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(detected_paths):
                    rfactor_path = str(detected_paths[idx])
                    break
                elif idx == len(detected_paths):
                    # Custom path
                    custom_path = input("Enter rFactor installation path: ").strip()
                    if custom_path:
                        rfactor_path = custom_path
                        break
            print(f"[ERROR] Invalid choice. Please enter 1-{len(detected_paths) + 1}")
    else:
        print("No rFactor installations detected automatically.")
        rfactor_path = input("Enter rFactor installation path: ").strip()

    if not rfactor_path:
        print("[ERROR] No path provided. Exiting.")
        sys.exit(1)

    # Validate the path
    print_section("Validating Installation")

    if not validate_and_show_info(rfactor_path):
        print()
        print("[ERROR] Please provide a valid rFactor installation path.")
        sys.exit(1)

    # Save rFactor path
    try:
        config.set_rfactor_path(rfactor_path, validate=True)
        print()
        print("[OK] rFactor path saved to configuration")
    except RFactorValidationError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Select player profile
    player_name = select_player_profile(rfactor_path)
    config.set_current_player(player_name)
    print(f"[OK] Player profile set to: {player_name}")

    # Show configuration summary
    print_section("Configuration Summary")

    summary = config.get_config_summary()
    print(f"Configuration file: {summary['config_file']}")
    print(f"rFactor path: {summary['rfactor_path']}")
    print(f"Current player: {summary['current_player']}")
    print(f"Talents available: {summary.get('talent_count', 0)}")
    print(f"Vehicles available: {summary.get('vehicle_count', 0)}")
    print(f"Locations available: {summary.get('location_count', 0)}")

    print_header("Configuration Complete!")
    print("You can now run the application.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
