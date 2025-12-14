"""
Service for managing rFactor tracks (locations).

Provides high-level operations for working with track .gdb files.
"""

from pathlib import Path
from typing import Optional

from ..models.track import Track
from ..parsers.gdb_parser import GdbParser
from ..utils.config import get_config


class TrackService:
    """Service for managing tracks."""

    def __init__(self):
        self.config = get_config()
        self.parser = GdbParser()
        self._tracks_cache: Optional[list[Track]] = None

    def get_locations_directory(self) -> Path:
        """
        Get the path to the locations directory (GameData/Locations).

        Returns:
            Path to GameData/Locations directory

        Raises:
            ValueError: If rFactor path is not configured
            FileNotFoundError: If the Locations directory does not exist
        """
        rfactor_path = self.config.get_rfactor_path()
        if not rfactor_path:
            raise ValueError("rFactor path is not configured. Please set 'rfactor_path' in configuration.")

        locations_dir = Path(rfactor_path) / 'GameData' / 'Locations'
        if not locations_dir.exists():
            raise FileNotFoundError(f"Locations directory not found: {locations_dir}")
        return locations_dir

    def list_all(self, force_reload: bool = False) -> list[Track]:
        if self._tracks_cache is None or force_reload:
            locations_dir = self.get_locations_directory()
            self._tracks_cache = self.parser.scan_directory(locations_dir)
        return self._tracks_cache

    def get_by_relative_path(self, relative_path: str) -> Optional[Track]:
        locations_dir = self.get_locations_directory()

        # Normalize incoming path
        rel = str(relative_path).replace("\\", "/").strip()
        rel_lower = rel.lower()
        # Strip leading GameData/Locations prefix if present (any case)
        for prefix in ("gamedata/locations/", "locations/", "/gamedata/locations/", "gamedata\\locations\\"):
            if rel_lower.startswith(prefix.replace("\\", "/")):
                rel = rel[len(prefix):]
                rel_lower = rel.lower()
                break
        # Remove any leading slashes
        while rel.startswith("/"):
            rel = rel[1:]

        # Try direct path
        candidate = locations_dir / rel
        track: Optional[Track] = None
        if candidate.exists() and candidate.suffix.lower() == ".gdb":
            track = self.parser.parse_file(candidate)
        else:
            # If extension missing, try adding .gdb
            if not rel_lower.endswith(".gdb"):
                candidate2 = locations_dir / (rel + ".gdb")
                if candidate2.exists():
                    track = self.parser.parse_file(candidate2)

        # Ensure relative_path is populated
        if track and not getattr(track, "relative_path", ""):
            try:
                rp = Path(track.file_path).resolve().relative_to(locations_dir.resolve())
                track.relative_path = str(rp).replace("\\", "/")
            except Exception:
                track.relative_path = rel if rel_lower.endswith(".gdb") else (rel + ".gdb")

        return track

    def search(
        self,
        query: str,
        search_track_name: bool = True,
        search_venue_name: bool = True,
        search_layout: bool = True,
        search_file_name: bool = True,
        force_reload: bool = False
    ) -> list[Track]:
        """
        Search tracks with configurable field selection.

        Args:
            query: Search query string
            search_track_name: Search in track name field
            search_venue_name: Search in venue name field
            search_layout: Search in layout field
            search_file_name: Search in file name field
            force_reload: Force reload from disk

        Returns:
            List of matching tracks
        """
        tracks = self.list_all(force_reload)
        return self.parser.search(
            tracks,
            query,
            search_track_name=search_track_name,
            search_venue_name=search_venue_name,
            search_layout=search_layout,
            search_file_name=search_file_name
        )
