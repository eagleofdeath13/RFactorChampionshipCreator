"""
Service for managing rFactor vehicles.

Provides high-level operations for working with vehicle files.
"""

from pathlib import Path
from typing import Optional

from ..models.vehicle import Vehicle
from ..parsers.veh_parser import VehParser
from ..generators.veh_generator import VehGenerator
from ..utils.config import get_config


class VehicleService:
    """Service for managing vehicles."""

    def __init__(self):
        """Initialize the vehicle service."""
        self.config = get_config()
        self.parser = VehParser()
        self.generator = VehGenerator()
        self._vehicles_cache: Optional[list[Vehicle]] = None

    def get_vehicles_directory(self) -> Path:
        """
        Get the path to the vehicles directory.

        Returns:
            Path to GameData/Vehicles directory

        Raises:
            ValueError: If rFactor path is not configured
            FileNotFoundError: If the Vehicles directory does not exist
        """
        rfactor_path = self.config.get_rfactor_path()
        if not rfactor_path:
            raise ValueError("rFactor path is not configured. Please set 'rfactor_path' in configuration.")

        vehicles_dir = Path(rfactor_path) / 'GameData' / 'Vehicles'
        if not vehicles_dir.exists():
            raise FileNotFoundError(f"Vehicles directory not found: {vehicles_dir}")

        return vehicles_dir

    def list_all(self, force_reload: bool = False) -> list[Vehicle]:
        """
        List all vehicles from the rFactor installation.

        Args:
            force_reload: If True, force reload from disk even if cached

        Returns:
            List of all vehicles
        """
        if self._vehicles_cache is None or force_reload:
            vehicles_dir = self.get_vehicles_directory()
            self._vehicles_cache = self.parser.scan_directory(vehicles_dir)

        return self._vehicles_cache

    def get_by_filename(self, filename: str) -> Optional[Vehicle]:
        """
        Get a vehicle by its filename.

        Args:
            filename: Vehicle filename (e.g., "Campana_27.veh")

        Returns:
            Vehicle if found, None otherwise
        """
        vehicles = self.list_all()
        for vehicle in vehicles:
            if vehicle.file_name == filename:
                return vehicle
        return None

    def get_by_relative_path(self, relative_path: str) -> Optional[Vehicle]:
        """
        Get a vehicle by its relative path from GameData/Vehicles.

        Args:
            relative_path: Relative path (e.g., "Howston/SRGP/Campana/Campana_27.veh")

        Returns:
            Vehicle if found, None otherwise
        """
        vehicles_dir = self.get_vehicles_directory()

        # Normalize incoming path
        rel = str(relative_path).replace("\\", "/").strip()
        rel_lower = rel.lower()
        # Strip leading GameData/Vehicles prefix if present (any case)
        for prefix in ("gamedata/vehicles/", "vehicles/", "/gamedata/vehicles/", "gamedata\\vehicles\\"):
            if rel_lower.startswith(prefix.replace("\\", "/")):
                rel = rel[len(prefix):]
                rel_lower = rel.lower()
                break
        # Remove any leading slashes
        while rel.startswith("/"):
            rel = rel[1:]

        # Try direct path
        candidate = vehicles_dir / rel
        vehicle = None
        if candidate.exists():
            vehicle = self.parser.parse_file(candidate)
        else:
            # If extension missing or wrong case, try adding .veh
            if not rel_lower.endswith(".veh"):
                candidate2 = vehicles_dir / (rel + ".veh")
                if candidate2.exists():
                    vehicle = self.parser.parse_file(candidate2)

        # Ensure relative_path is populated
        if vehicle and not getattr(vehicle, "relative_path", ""):
            try:
                rp = Path(vehicle.file_path).resolve().relative_to(vehicles_dir.resolve())
                vehicle.relative_path = str(rp).replace("\\", "/")
            except Exception:
                vehicle.relative_path = rel

        return vehicle

    def filter_by_class(self, class_name: str, force_reload: bool = False) -> list[Vehicle]:
        """
        Get all vehicles of a specific class.

        Args:
            class_name: Class name to filter by (e.g., "SRGP")
            force_reload: If True, force reload from disk

        Returns:
            List of vehicles with the specified class
        """
        vehicles = self.list_all(force_reload)
        return self.parser.get_vehicles_by_class(vehicles, class_name)

    def get_unique_classes(self, force_reload: bool = False) -> set[str]:
        """
        Get all unique vehicle classes.

        Args:
            force_reload: If True, force reload from disk

        Returns:
            Set of unique class names
        """
        vehicles = self.list_all(force_reload)
        return self.parser.get_unique_classes(vehicles)

    def get_unique_manufacturers(self, force_reload: bool = False) -> set[str]:
        """
        Get all unique manufacturers.

        Args:
            force_reload: If True, force reload from disk

        Returns:
            Set of unique manufacturer names
        """
        vehicles = self.list_all(force_reload)
        manufacturers = {v.manufacturer for v in vehicles if v.manufacturer}
        return manufacturers

    def filter_by_manufacturer(self, manufacturer: str, force_reload: bool = False) -> list[Vehicle]:
        """
        Get all vehicles from a specific manufacturer.

        Args:
            manufacturer: Manufacturer name
            force_reload: If True, force reload from disk

        Returns:
            List of vehicles from the manufacturer
        """
        vehicles = self.list_all(force_reload)
        return [v for v in vehicles if v.manufacturer == manufacturer]

    def search(
        self,
        query: str,
        search_driver: bool = True,
        search_team: bool = True,
        search_description: bool = True,
        force_reload: bool = False
    ) -> list[Vehicle]:
        """
        Search for vehicles by query string.

        Args:
            query: Search query
            search_driver: Include driver name in search
            search_team: Include team name in search
            search_description: Include description in search
            force_reload: If True, force reload from disk

        Returns:
            List of matching vehicles
        """
        if not query:
            return []

        query_lower = query.lower()
        vehicles = self.list_all(force_reload)
        results = []

        for vehicle in vehicles:
            # Check driver name
            if search_driver and vehicle.team_info.driver:
                if query_lower in vehicle.team_info.driver.lower():
                    results.append(vehicle)
                    continue

            # Check team name
            if search_team and vehicle.team_info.team:
                if query_lower in vehicle.team_info.team.lower():
                    results.append(vehicle)
                    continue

            # Check description
            if search_description and vehicle.description:
                if query_lower in vehicle.description.lower():
                    results.append(vehicle)
                    continue

        return results

    def count_vehicles(self, force_reload: bool = False) -> int:
        """
        Get total count of vehicles.

        Args:
            force_reload: If True, force reload from disk

        Returns:
            Number of vehicles
        """
        return len(self.list_all(force_reload))

    def clear_cache(self):
        """Clear the vehicles cache to force reload on next access."""
        self._vehicles_cache = None

    def update(self, relative_path: str, driver: Optional[str] = None) -> Vehicle:
        """
        Update a vehicle file with new information.

        Args:
            relative_path: Relative path to the vehicle file from GameData/Vehicles
            driver: New driver name (if None, keeps existing driver)

        Returns:
            Updated Vehicle object

        Raises:
            FileNotFoundError: If vehicle file not found
            ValueError: If update fails
        """
        # Get the vehicle
        vehicle = self.get_by_relative_path(relative_path)
        if not vehicle:
            raise FileNotFoundError(f"Vehicle not found: {relative_path}")

        # Update the fields
        if driver is not None:
            vehicle.team_info.driver = driver

        # Write the updated vehicle back to disk
        vehicles_dir = self.get_vehicles_directory()
        file_path = vehicles_dir / vehicle.relative_path

        self.generator.write_file(vehicle, file_path)

        # Clear cache to ensure fresh data on next read
        self.clear_cache()

        # Re-parse the file to ensure it was written correctly
        updated_vehicle = self.parser.parse_file(file_path)
        if not updated_vehicle:
            raise ValueError(f"Failed to verify updated vehicle file: {file_path}")

        return updated_vehicle
