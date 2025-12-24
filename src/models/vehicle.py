"""
Vehicle data model for rFactor .veh files.

Represents a vehicle with its configuration, team information, and metadata.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VehicleTeamInfo:
    """Team and driver information for a vehicle."""

    team: str = ""  # Team name
    full_team_name: str = ""  # Full team name
    driver: str = ""  # Driver name
    pit_group: str = "Group1"  # Pit group
    team_founded: Optional[int] = None  # Year team was founded
    team_headquarters: str = ""  # Team headquarters location
    team_starts: int = 0  # Number of starts
    team_poles: int = 0  # Number of poles
    team_wins: int = 0  # Number of wins
    team_world_championships: int = 0  # Number of championships


@dataclass
class VehicleConfig:
    """Technical configuration for a vehicle."""

    default_livery: str = ""  # Default livery file (e.g., "Campana_27.DDS")
    gen_string: str = ""  # GenString value from .veh

    # HDV file reference
    hdvehicle: str = ""
    hdvehicle_resolved: str = ""  # Resolved absolute path
    hdvehicle_exists: bool = False  # Whether file exists

    # Graphics file reference (.gen)
    graphics: str = ""
    graphics_resolved: str = ""
    graphics_exists: bool = False

    # Spinner file reference (.gen)
    spinner: str = ""
    spinner_resolved: str = ""
    spinner_exists: bool = False

    # Upgrades file reference (.ini)
    upgrades: str = ""
    upgrades_resolved: str = ""
    upgrades_exists: bool = False

    # Sounds file reference (.sfx)
    sounds: str = ""
    sounds_resolved: str = ""
    sounds_exists: bool = False

    # Cameras file reference (.cam)
    cameras: str = ""
    cameras_resolved: str = ""
    cameras_exists: bool = False

    # Head physics file reference (.ini)
    head_physics: str = ""
    head_physics_resolved: str = ""
    head_physics_exists: bool = False

    # Cockpit file reference (.ini)
    cockpit: str = ""
    cockpit_resolved: str = ""
    cockpit_exists: bool = False

    # AI upgrade class
    ai_upgrade_class: str = ""


@dataclass
class Vehicle:
    """
    Represents an rFactor vehicle (.veh file).

    Contains all information about a vehicle including technical configuration,
    team information, and metadata.
    """

    # Basic identification
    number: int = 0  # Vehicle number
    description: str = ""  # Vehicle description (e.g., "Campana #27")
    engine: str = ""  # Engine name/type
    manufacturer: str = ""  # Manufacturer name
    classes: str = ""  # Vehicle classes (space-separated)
    category: str = ""  # Vehicle category

    # Team and driver info
    team_info: VehicleTeamInfo = field(default_factory=VehicleTeamInfo)

    # Technical configuration
    config: VehicleConfig = field(default_factory=VehicleConfig)

    # File metadata
    file_path: str = ""  # Full path to .veh file
    file_name: str = ""  # Just the filename (e.g., "Campana_27.veh")
    relative_path: str = ""  # Path relative to GameData/Vehicles

    def __post_init__(self):
        """Post-initialization to set file_name from file_path if not set."""
        if self.file_path and not self.file_name:
            from pathlib import Path
            self.file_name = Path(self.file_path).name

    @property
    def display_name(self) -> str:
        """Get a display-friendly name for the vehicle."""
        if self.description:
            return self.description
        if self.team_info.driver and self.number:
            return f"{self.team_info.driver} #{self.number}"
        if self.number:
            return f"Vehicle #{self.number}"
        return self.file_name or "Unknown Vehicle"

    @property
    def class_list(self) -> list[str]:
        """Get vehicle classes as a list."""
        if not self.classes:
            return []
        return [c.strip() for c in self.classes.split() if c.strip()]

    def has_class(self, class_name: str) -> bool:
        """Check if vehicle has a specific class."""
        return class_name in self.class_list
