"""
Utilities for validating and detecting rFactor installations.

This module provides functions to verify that a directory is a valid rFactor installation.
"""

from pathlib import Path
from typing import Tuple, List


class RFactorValidationError(Exception):
    """Exception raised when rFactor validation fails."""
    pass


class RFactorValidator:
    """Validator for rFactor installations."""

    # Required files/directories for a valid rFactor installation
    REQUIRED_ITEMS = [
        "rFactor.exe",           # Main executable
        "GameData",              # GameData directory
        "UserData",              # UserData directory
    ]

    # Additional items that should exist in GameData
    GAMEDATA_ITEMS = [
        "Talent",                # Talent directory
        "Vehicles",              # Vehicles directory
        "Locations",             # Locations directory
    ]

    @staticmethod
    def validate(path: str) -> Tuple[bool, List[str]]:
        """
        Validate if a directory is a valid rFactor installation.

        Args:
            path: Path to check

        Returns:
            Tuple of (is_valid, list_of_missing_items)

        Example:
            >>> is_valid, missing = RFactorValidator.validate("C:/rFactor")
            >>> if not is_valid:
            ...     print(f"Missing: {missing}")
        """
        rfactor_path = Path(path)
        missing_items = []

        # Check if path exists and is a directory
        if not rfactor_path.exists():
            return False, ["Directory does not exist"]

        if not rfactor_path.is_dir():
            return False, ["Path is not a directory"]

        # Check required items at root level
        for item in RFactorValidator.REQUIRED_ITEMS:
            item_path = rfactor_path / item
            if not item_path.exists():
                missing_items.append(item)

        # If GameData exists, check its contents
        gamedata_path = rfactor_path / "GameData"
        if gamedata_path.exists():
            for item in RFactorValidator.GAMEDATA_ITEMS:
                item_path = gamedata_path / item
                if not item_path.exists():
                    missing_items.append(f"GameData/{item}")

        is_valid = len(missing_items) == 0
        return is_valid, missing_items

    @staticmethod
    def validate_or_raise(path: str) -> None:
        """
        Validate a directory and raise an exception if invalid.

        Args:
            path: Path to validate

        Raises:
            RFactorValidationError: If the path is not a valid rFactor installation
        """
        is_valid, missing_items = RFactorValidator.validate(path)

        if not is_valid:
            missing_str = ", ".join(missing_items)
            raise RFactorValidationError(
                f"Invalid rFactor installation at '{path}'. "
                f"Missing: {missing_str}"
            )

    @staticmethod
    def get_version_info(path: str) -> dict:
        """
        Get version information from rFactor installation.

        Args:
            path: Path to rFactor installation

        Returns:
            Dictionary with version info (if available)
        """
        rfactor_path = Path(path)
        info = {
            "path": str(rfactor_path.absolute()),
            "exists": rfactor_path.exists(),
            "is_valid": False,
        }

        is_valid, _ = RFactorValidator.validate(path)
        info["is_valid"] = is_valid

        if is_valid:
            # Count talents, vehicles, locations
            gamedata = rfactor_path / "GameData"

            talent_dir = gamedata / "Talent"
            if talent_dir.exists():
                rcd_files = list(talent_dir.glob("*.rcd"))
                # Exclude Dialog.ini if present
                rcd_files = [f for f in rcd_files if f.stem != "Dialog"]
                info["talent_count"] = len(rcd_files)

            vehicles_dir = gamedata / "Vehicles"
            if vehicles_dir.exists():
                veh_files = list(vehicles_dir.glob("**/*.veh"))
                info["vehicle_count"] = len(veh_files)

            locations_dir = gamedata / "Locations"
            if locations_dir.exists():
                gdb_files = list(locations_dir.glob("**/*.gdb"))
                info["location_count"] = len(gdb_files)

        return info

    @staticmethod
    def find_user_data_dir(path: str) -> Path:
        """
        Get the UserData directory path.

        Args:
            path: Path to rFactor installation

        Returns:
            Path to UserData directory

        Raises:
            RFactorValidationError: If UserData directory doesn't exist
        """
        rfactor_path = Path(path)
        userdata_path = rfactor_path / "UserData"

        if not userdata_path.exists():
            raise RFactorValidationError(
                f"UserData directory not found at '{userdata_path}'"
            )

        return userdata_path

    @staticmethod
    def list_player_profiles(path: str) -> List[str]:
        """
        List all player profiles in UserData.

        Args:
            path: Path to rFactor installation

        Returns:
            List of player profile names (directory names)
        """
        userdata_path = RFactorValidator.find_user_data_dir(path)

        # List all subdirectories in UserData
        profiles = []
        for item in userdata_path.iterdir():
            if item.is_dir():
                profiles.append(item.name)

        return sorted(profiles)
