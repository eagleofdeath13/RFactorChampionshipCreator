"""
Configuration management for rFactor Championship Creator.

Handles storing and retrieving application configuration, including rFactor path.
"""

import json
from pathlib import Path
from typing import Optional

from .rfactor_validator import RFactorValidator, RFactorValidationError


class Config:
    """Application configuration manager."""

    # Default config file location (in user's home directory or app directory)
    DEFAULT_CONFIG_FILE = "config.json"

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to config file. If None, uses default location.
        """
        if config_file is None:
            # Store config in the project root
            config_file = self.DEFAULT_CONFIG_FILE

        self.config_file = Path(config_file)
        self.data = self._load_config()

    def _load_config(self) -> dict:
        """
        Load configuration from file.

        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            return self._default_config()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            # If config is corrupted, return default
            return self._default_config()

    def _default_config(self) -> dict:
        """
        Get default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            "rfactor_path": None,
            "current_player": None,
            "last_championship": None,
            "recent_championships": [],
        }

    def save(self) -> None:
        """Save configuration to file."""
        # Ensure parent directory exists
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def get_rfactor_path(self) -> Optional[str]:
        """
        Get the configured rFactor path.

        Returns:
            Path to rFactor installation or None if not configured
        """
        return self.data.get("rfactor_path")

    def set_rfactor_path(self, path: str, validate: bool = True) -> None:
        """
        Set the rFactor installation path.

        Args:
            path: Path to rFactor installation
            validate: Whether to validate the path before saving

        Raises:
            RFactorValidationError: If validate=True and path is invalid
        """
        if validate:
            RFactorValidator.validate_or_raise(path)

        # Store as absolute path
        abs_path = str(Path(path).absolute())
        self.data["rfactor_path"] = abs_path
        self.save()

    def get_current_player(self) -> Optional[str]:
        """
        Get the current player profile name.

        Returns:
            Player profile name or None if not set
        """
        return self.data.get("current_player")

    def set_current_player(self, player_name: str) -> None:
        """
        Set the current player profile.

        Args:
            player_name: Name of the player profile
        """
        self.data["current_player"] = player_name
        self.save()

    def add_recent_championship(self, championship_name: str, max_recent: int = 10) -> None:
        """
        Add a championship to recent championships list.

        Args:
            championship_name: Name of the championship
            max_recent: Maximum number of recent items to keep
        """
        recent = self.data.get("recent_championships", [])

        # Remove if already in list
        if championship_name in recent:
            recent.remove(championship_name)

        # Add to beginning
        recent.insert(0, championship_name)

        # Keep only max_recent items
        recent = recent[:max_recent]

        self.data["recent_championships"] = recent
        self.save()

    def get_recent_championships(self) -> list:
        """
        Get list of recent championships.

        Returns:
            List of championship names
        """
        return self.data.get("recent_championships", [])

    def is_configured(self) -> bool:
        """
        Check if the application is properly configured.

        Returns:
            True if rFactor path is set and valid
        """
        rfactor_path = self.get_rfactor_path()
        if not rfactor_path:
            return False

        is_valid, _ = RFactorValidator.validate(rfactor_path)
        return is_valid

    def get_config_summary(self) -> dict:
        """
        Get a summary of current configuration.

        Returns:
            Dictionary with configuration summary
        """
        rfactor_path = self.get_rfactor_path()

        summary = {
            "is_configured": self.is_configured(),
            "rfactor_path": rfactor_path,
            "current_player": self.get_current_player(),
            "config_file": str(self.config_file.absolute()),
        }

        if rfactor_path:
            try:
                info = RFactorValidator.get_version_info(rfactor_path)
                summary.update({
                    "rfactor_valid": info.get("is_valid", False),
                    "talent_count": info.get("talent_count", 0),
                    "vehicle_count": info.get("vehicle_count", 0),
                    "location_count": info.get("location_count", 0),
                })

                if info.get("is_valid"):
                    players = RFactorValidator.list_player_profiles(rfactor_path)
                    summary["available_players"] = players
            except Exception:
                summary["rfactor_valid"] = False

        return summary

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.data = self._default_config()
        self.save()


# Global config instance
_config_instance: Optional[Config] = None


def get_config(config_file: Optional[str] = None) -> Config:
    """
    Get the global configuration instance.

    Args:
        config_file: Path to config file (only used on first call)

    Returns:
        Config instance
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = Config(config_file)

    return _config_instance
