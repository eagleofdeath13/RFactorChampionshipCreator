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

            # Calculate relative path from GameData/Vehicles
            try:
                # Find GameData/Vehicles in the path
                parts = file_path_obj.parts
                if 'GameData' in parts and 'Vehicles' in parts:
                    gd_idx = parts.index('GameData')
                    v_idx = parts.index('Vehicles')
                    if v_idx == gd_idx + 1:
                        # Get everything after Vehicles/
                        rel_parts = parts[v_idx + 1:]
                        vehicle.relative_path = str(Path(*rel_parts)) if rel_parts else ""

                        # Resolve HDV absolute path if reference present
                        if config.hdvehicle:
                            # Base directory is the Vehicles directory (C:\...\GameData\Vehicles)
                            vehicles_root = Path(*parts[:v_idx + 1])
                            # Normalize separators in reference
                            ref = config.hdvehicle.replace('/', '\\')
                            ref_path = Path(ref)

                            def _resolve_hdv_from_vehicle_dir(base_dir: Path, ref_p: Path, root: Path) -> Path:
                                """Resolve HDV path by walking up from vehicle directory to Vehicles root when ref is a bare filename."""
                                # If ref includes dirs, resolve from Vehicles root directly
                                if ref_p.is_absolute():
                                    return ref_p
                                if len(ref_p.parts) > 1:
                                    return root / ref_p

                                # Bare filename: walk up from .veh directory to Vehicles root
                                current = base_dir
                                try:
                                    root_resolved = root.resolve()
                                except Exception:
                                    root_resolved = root

                                while True:
                                    candidate = current / ref_p
                                    try:
                                        if candidate.exists():
                                            return candidate
                                    except Exception:
                                        # If existence check fails, still return candidate to expose path
                                        return candidate

                                    # Stop when we've reached the Vehicles root
                                    try:
                                        if current.resolve() == root_resolved:
                                            break
                                    except Exception:
                                        # Fallback to string comparison if resolve fails
                                        if str(current) == str(root):
                                            break

                                    parent = current.parent
                                    if parent == current:
                                        break
                                    current = parent

                                # Fallback to Vehicles root + filename
                                return root / ref_p

                            hdv_path = _resolve_hdv_from_vehicle_dir(file_path_obj.parent, ref_path, vehicles_root)
                            try:
                                config.hdvehicle_resolved = str(hdv_path)
                                config.hdvehicle_exists = hdv_path.exists()
                            except Exception:
                                config.hdvehicle_resolved = str(hdv_path)
                                config.hdvehicle_exists = False
            except (ValueError, IndexError):
                vehicle.relative_path = ""
                # Fallback HDV resolve with global config if possible
                try:
                    if config.hdvehicle:
                        rfactor_path = self.config.get_rfactor_path()
                        if rfactor_path:
                            vehicles_root = Path(rfactor_path) / 'GameData' / 'Vehicles'
                            ref = config.hdvehicle.replace('/', '\\')
                            ref_path = Path(ref)
                            # Use same resolution strategy as above
                            def _resolve_hdv_from_root_only(ref_p: Path, root: Path) -> Path:
                                if ref_p.is_absolute():
                                    return ref_p
                                if len(ref_p.parts) > 1:
                                    return root / ref_p
                                # Bare filename: try one-level heuristic using folder name equal to filename stem
                                candidate = root / ref_p.stem / ref_p
                                try:
                                    if candidate.exists():
                                        return candidate
                                except Exception:
                                    pass
                                return root / ref_p

                            hdv_path = _resolve_hdv_from_root_only(ref_path, vehicles_root)
                            config.hdvehicle_resolved = str(hdv_path)
                            config.hdvehicle_exists = hdv_path.exists()
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
