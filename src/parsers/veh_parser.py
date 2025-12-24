"""
Parser for rFactor .veh (vehicle) files.

Parses vehicle configuration files to extract vehicle information, team data,
and technical configuration.
"""

import re
from pathlib import Path
from typing import Optional

from ..models.vehicle import Vehicle, VehicleTeamInfo, VehicleConfig
from ..utils.config import get_config


class VehParser:
    """Parser for .veh vehicle files."""

    def __init__(self):
        """Initialize the parser."""
        self.config = get_config()

    def parse_file(self, file_path: str | Path) -> Optional[Vehicle]:
        """
        Parse a .veh file and return a Vehicle object.

        Args:
            file_path: Path to the .veh file

        Returns:
            Vehicle object if parsing succeeds, None otherwise
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return None

        try:
            # Read file with Windows-1252 encoding (common for rFactor files)
            with open(file_path, 'r', encoding='windows-1252', errors='ignore') as f:
                content = f.read()

            return self.parse_content(content, str(file_path))

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def parse_content(self, content: str, file_path: str = "") -> Vehicle:
        """
        Parse the content of a .veh file.

        Args:
            content: String content of the .veh file
            file_path: Optional file path for metadata

        Returns:
            Vehicle object
        """
        vehicle = Vehicle()
        team_info = VehicleTeamInfo()
        config = VehicleConfig()

        # Parse each line
        for line in content.split('\n'):
            # Remove comments and whitespace
            line = line.split('//')[0].strip()

            if not line or line.startswith('//'):
                continue

            # Try to parse as key=value
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')  # Remove quotes

                # Parse configuration fields
                if key == 'DefaultLivery':
                    config.default_livery = value
                elif key == 'HDVehicle':
                    config.hdvehicle = value
                elif key == 'GenString':
                    config.gen_string = value
                elif key == 'Graphics':
                    config.graphics = value
                elif key == 'Spinner':
                    config.spinner = value
                elif key == 'Upgrades':
                    config.upgrades = value
                elif key == 'Sounds':
                    config.sounds = value
                elif key == 'Cameras':
                    config.cameras = value
                elif key == 'HeadPhysics':
                    config.head_physics = value
                elif key == 'Cockpit':
                    config.cockpit = value
                elif key == 'AIUpgradeClass':
                    config.ai_upgrade_class = value

                # Parse vehicle fields
                elif key == 'Number':
                    try:
                        vehicle.number = int(value)
                    except ValueError:
                        vehicle.number = 0
                elif key == 'Description':
                    vehicle.description = value
                elif key == 'Engine':
                    vehicle.engine = value
                elif key == 'Manufacturer':
                    vehicle.manufacturer = value
                elif key == 'Classes':
                    vehicle.classes = value
                elif key == 'Category':
                    vehicle.category = value

                # Parse team info fields
                elif key == 'Team':
                    team_info.team = value
                elif key == 'FullTeamName':
                    team_info.full_team_name = value
                elif key == 'Driver':
                    team_info.driver = value
                elif key == 'PitGroup':
                    team_info.pit_group = value
                elif key == 'TeamFounded':
                    try:
                        team_info.team_founded = int(value) if value.lower() != 'n/a' else None
                    except ValueError:
                        team_info.team_founded = None
                elif key == 'TeamHeadquarters':
                    team_info.team_headquarters = value
                elif key == 'TeamStarts':
                    try:
                        team_info.team_starts = int(value) if value.lower() != 'n/a' else 0
                    except ValueError:
                        team_info.team_starts = 0
                elif key == 'TeamPoles':
                    try:
                        team_info.team_poles = int(value) if value.lower() != 'n/a' else 0
                    except ValueError:
                        team_info.team_poles = 0
                elif key == 'TeamWins':
                    try:
                        team_info.team_wins = int(value) if value.lower() != 'n/a' else 0
                    except ValueError:
                        team_info.team_wins = 0
                elif key == 'TeamWorldChampionships':
                    try:
                        team_info.team_world_championships = int(value) if value.lower() != 'n/a' else 0
                    except ValueError:
                        team_info.team_world_championships = 0

        # Set the parsed data
        vehicle.team_info = team_info
        vehicle.config = config

        # Set file metadata
        if file_path:
            vehicle.file_path = file_path
            file_path_obj = Path(file_path)
            vehicle.file_name = file_path_obj.name

            # Calculate relative path from Vehicles directory
            try:
                # Find Vehicles in the path (works for both GameData/Vehicles and RFactorContent/Vehicles)
                parts = file_path_obj.parts
                if 'Vehicles' in parts:
                    v_idx = parts.index('Vehicles')

                    # Get everything after Vehicles/
                    rel_parts = parts[v_idx + 1:]
                    vehicle.relative_path = str(Path(*rel_parts)) if rel_parts else ""

                    # Resolve technical file paths (HDV, Graphics, Sounds, etc.)
                    # Base directory is the Vehicles directory
                    vehicles_root = Path(*parts[:v_idx + 1])

                    # Determine mod root (first child of Vehicles/)
                    # This prevents searching outside the mod directory
                    mod_root = None
                    if len(parts) > v_idx + 1:
                        mod_root = Path(*parts[:v_idx + 2])  # Vehicles/ModName

                    def _resolve_technical_file(base_dir: Path, ref_str: str, vehicles_root: Path, mod_root: Path | None) -> tuple[str, bool]:
                        """
                        Resolve technical file path generically.

                        Strategy:
                        1. Search from .veh directory upwards to mod root
                        2. If not found, search in Vehicles root (global files)

                        This approach works for both structures:
                        - Vanilla: Vehicles/ModName/Season/Class/Team/file.veh
                        - All_Teams: Vehicles/ModName/All_Teams/Team/file.veh

                        Args:
                            base_dir: Directory containing the .veh file
                            ref_str: File reference from .veh (e.g., "Boxer\\Boxer.hdv")
                            vehicles_root: Root Vehicles directory
                            mod_root: Root of the mod (first child of Vehicles/)

                        Returns:
                            Tuple of (resolved_path_str, exists_bool)
                        """
                        if not ref_str:
                            return "", False

                        # Normalize separators
                        ref = ref_str.replace('/', '\\')
                        ref_path = Path(ref)

                        # If absolute path, use as-is
                        if ref_path.is_absolute():
                            try:
                                return str(ref_path), ref_path.exists()
                            except Exception:
                                return str(ref_path), False

                        # Strategy 1: Walk up from .veh directory to mod root
                        current = base_dir
                        try:
                            vehicles_root_resolved = vehicles_root.resolve()
                        except Exception:
                            vehicles_root_resolved = vehicles_root

                        try:
                            mod_root_resolved = mod_root.resolve() if mod_root else None
                        except Exception:
                            mod_root_resolved = mod_root

                        while True:
                            # Try resolving the reference from current directory
                            candidate = current / ref_path
                            try:
                                if candidate.exists():
                                    return str(candidate), True
                            except Exception:
                                pass

                            # Stop at mod root (don't go above it)
                            if mod_root_resolved:
                                try:
                                    if current.resolve() == mod_root_resolved:
                                        break
                                except Exception:
                                    if str(current) == str(mod_root):
                                        break

                            # Stop at Vehicles root
                            try:
                                if current.resolve() == vehicles_root_resolved:
                                    break
                            except Exception:
                                if str(current) == str(vehicles_root):
                                    break

                            # Move to parent
                            parent = current.parent
                            if parent == current:
                                break
                            current = parent

                        # Strategy 2: Try from mod root directly (if we haven't checked it yet)
                        if mod_root:
                            candidate = mod_root / ref_path
                            try:
                                if candidate.exists():
                                    return str(candidate), True
                            except Exception:
                                pass

                        # Strategy 3: Fallback to Vehicles root (global files)
                        candidate = vehicles_root / ref_path
                        try:
                            return str(candidate), candidate.exists()
                        except Exception:
                            return str(candidate), False

                    # Resolve ALL technical file paths
                    if config.hdvehicle:
                        config.hdvehicle_resolved, config.hdvehicle_exists = _resolve_technical_file(
                            file_path_obj.parent, config.hdvehicle, vehicles_root, mod_root
                        )
                    if config.graphics:
                        config.graphics_resolved, config.graphics_exists = _resolve_technical_file(
                            file_path_obj.parent, config.graphics, vehicles_root, mod_root
                        )
                    if config.spinner:
                        config.spinner_resolved, config.spinner_exists = _resolve_technical_file(
                            file_path_obj.parent, config.spinner, vehicles_root, mod_root
                        )
                    if config.upgrades:
                        config.upgrades_resolved, config.upgrades_exists = _resolve_technical_file(
                            file_path_obj.parent, config.upgrades, vehicles_root, mod_root
                        )
                    if config.sounds:
                        config.sounds_resolved, config.sounds_exists = _resolve_technical_file(
                            file_path_obj.parent, config.sounds, vehicles_root, mod_root
                        )
                    if config.cameras:
                        config.cameras_resolved, config.cameras_exists = _resolve_technical_file(
                            file_path_obj.parent, config.cameras, vehicles_root, mod_root
                        )
                    if config.head_physics:
                        config.head_physics_resolved, config.head_physics_exists = _resolve_technical_file(
                            file_path_obj.parent, config.head_physics, vehicles_root, mod_root
                        )
                    if config.cockpit:
                        config.cockpit_resolved, config.cockpit_exists = _resolve_technical_file(
                            file_path_obj.parent, config.cockpit, vehicles_root, mod_root
                        )
            except (ValueError, IndexError):
                vehicle.relative_path = ""
                # Fallback: try to resolve HDV with just Vehicles root if path info unavailable
                try:
                    if config.hdvehicle:
                        rfactor_path = self.config.get_rfactor_path()
                        if rfactor_path:
                            vehicles_root = Path(rfactor_path) / 'GameData' / 'Vehicles'
                            # Simple fallback: just try from Vehicles root
                            ref = config.hdvehicle.replace('/', '\\')
                            ref_path = Path(ref)
                            candidate = vehicles_root / ref_path
                            try:
                                config.hdvehicle_resolved = str(candidate)
                                config.hdvehicle_exists = candidate.exists()
                            except Exception:
                                config.hdvehicle_resolved = str(candidate)
                                config.hdvehicle_exists = False
                except Exception:
                    pass

        return vehicle

    def scan_directory(self, directory: str | Path) -> list[Vehicle]:
        """
        Scan a directory recursively for .veh files and parse them.

        Args:
            directory: Directory to scan

        Returns:
            List of Vehicle objects
        """
        directory = Path(directory)
        vehicles = []

        if not directory.exists():
            return vehicles

        # Find all .veh files recursively
        for veh_file in directory.rglob('*.veh'):
            vehicle = self.parse_file(veh_file)
            if vehicle:
                vehicles.append(vehicle)

        return vehicles

    def get_vehicles_by_class(self, vehicles: list[Vehicle], class_name: str) -> list[Vehicle]:
        """
        Filter vehicles by class.

        Args:
            vehicles: List of vehicles to filter
            class_name: Class name to filter by

        Returns:
            List of vehicles with the specified class
        """
        return [v for v in vehicles if v.has_class(class_name)]

    def get_unique_classes(self, vehicles: list[Vehicle]) -> set[str]:
        """
        Get all unique classes from a list of vehicles.

        Args:
            vehicles: List of vehicles

        Returns:
            Set of unique class names
        """
        classes = set()
        for vehicle in vehicles:
            classes.update(vehicle.class_list)
        return classes
