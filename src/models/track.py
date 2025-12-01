"""
Track data model for rFactor location (.gdb) files.

Represents a circuit with basic metadata extracted from .gdb files.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Track:
    """Represents an rFactor track (.gdb file)."""

    # Names
    track_name: str = ""  # TrackName in .gdb (often includes layout)
    venue_name: str = ""  # VenueName in .gdb (location/city)
    layout: str = ""      # Optional layout name

    # File metadata
    file_path: str = ""      # Full path to .gdb file
    file_name: str = ""      # Filename (e.g., "Toban_Short.gdb")
    relative_path: str = ""  # Path relative to GameData/Locations

    # Raw/extra info parsed from GDB (all key=value pairs)
    gdb_info: Dict[str, str] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        """Human friendly name."""
        if self.track_name:
            return self.track_name
        return self.file_name or "Unknown Track"
