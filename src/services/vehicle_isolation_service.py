"""
Service for isolating vehicles for custom championships.

This service copies selected vehicles to a championship-specific directory
and modifies their Classes and Driver fields.
"""

import shutil
from pathlib import Path
from typing import List, Dict, Optional, Set

from ..parsers.veh_parser import VehParser
from ..models.vehicle import Vehicle
from ..utils.dependency_collector import DependencyCollector


class VehicleIsolationService:
    """Service for isolating vehicles in championship-specific directories."""

    def __init__(self, rfactor_path: str):
        """
        Initialize service.

        Args:
            rfactor_path: Path to rFactor installation
        """
        self.rfactor_path = Path(rfactor_path)
        self.vehicles_dir = self.rfactor_path / "GameData" / "Vehicles"
        self.veh_parser = VehParser()
        self.dependency_collector = DependencyCollector()

    def _generate_vehicle_prefix(self, championship_name: str) -> str:
        """
        Generate a short prefix (2-3 chars) from championship name.

        Args:
            championship_name: Championship name

        Returns:
            Short prefix (e.g., "TC" for "TestChampionship")
        """
        # Take first letter of each word (up to 3)
        words = championship_name.replace('_', ' ').split()
        prefix = ''.join(word[0].upper() for word in words[:3])

        # Ensure at least 2 chars
        if len(prefix) < 2:
            prefix = championship_name[:2].upper()

        # Limit to 3 chars max
        return prefix[:3]

    def isolate_vehicles(
        self,
        championship_name: str,
        vehicle_assignments: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Isolate vehicles for a championship.

        Creates a championship-specific directory and copies selected vehicles
        with modified Classes and Driver fields.

        Args:
            championship_name: Name of the championship (will be prefixed with RFTOOL_)
            vehicle_assignments: List of dicts with keys:
                - 'vehicle_path': Relative path to original .veh file
                - 'driver_name': Name of driver to assign

        Returns:
            Dict mapping original paths to new isolated paths

        Raises:
            ValueError: If inputs are invalid
            FileNotFoundError: If vehicles directory doesn't exist
            IOError: If isolation fails for critical reasons

        Example:
            >>> service = VehicleIsolationService("/path/to/rFactor")
            >>> assignments = [
            ...     {
            ...         'vehicle_path': 'RHEZ/2005RHEZ/GT3/TEAM_YELLOW/YEL_09.veh',
            ...         'driver_name': 'John Doe'
            ...     }
            ... ]
            >>> result = service.isolate_vehicles("MyChamp2025", assignments)
        """
        # Validate inputs
        if not championship_name:
            raise ValueError("Championship name cannot be empty")
        if not vehicle_assignments:
            raise ValueError("Vehicle assignments list cannot be empty")

        # Validate vehicles directory exists
        if not self.vehicles_dir.exists():
            raise FileNotFoundError(f"Vehicles directory not found: {self.vehicles_dir}")

        # Create championship prefix
        champ_prefix = f"M_{championship_name}"
        champ_dir = self.vehicles_dir / champ_prefix

        # Create championship directory
        try:
            champ_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise IOError(f"Failed to create championship directory {champ_dir}: {e}")

        isolated_paths = {}
        failed_vehicles = []

        # Track shared files across all vehicles to avoid copying them multiple times
        copied_shared_files = set()

        for i, assignment in enumerate(vehicle_assignments):
            # Validate assignment structure
            if 'vehicle_path' not in assignment:
                print(f"Warning: Skipping assignment #{i+1}: missing 'vehicle_path'")
                continue
            if 'driver_name' not in assignment:
                print(f"Warning: Skipping assignment #{i+1}: missing 'driver_name'")
                continue

            vehicle_path = assignment['vehicle_path']
            driver_name = assignment['driver_name']

            # Isolate this vehicle
            try:
                new_path = self._isolate_single_vehicle(
                    vehicle_path,
                    champ_prefix,
                    championship_name,
                    driver_name,
                    copied_shared_files
                )
                isolated_paths[vehicle_path] = new_path
                print(f"  [OK] Isolated: {vehicle_path} -> {driver_name}")

            except FileNotFoundError as e:
                failed_vehicles.append((vehicle_path, str(e)))
                print(f"  [FAIL] Failed: {vehicle_path} - {e}")

            except (ValueError, IOError) as e:
                failed_vehicles.append((vehicle_path, str(e)))
                print(f"  [FAIL] Failed: {vehicle_path} - {e}")

        # Report summary
        if failed_vehicles:
            print(f"\nWarning: {len(failed_vehicles)} vehicle(s) failed to isolate")
            if len(isolated_paths) == 0:
                raise IOError(f"All vehicles failed to isolate. First error: {failed_vehicles[0][1]}")

        return isolated_paths

    def _isolate_single_vehicle(
        self,
        vehicle_path: str,
        champ_prefix: str,
        championship_name: str,
        driver_name: str,
        copied_shared_files: set
    ) -> str:
        """
        Isolate a single vehicle.

        Args:
            vehicle_path: Relative path to original vehicle
            champ_prefix: Championship prefix (RFTOOL_XXX)
            championship_name: Name of championship (for Classes)
            driver_name: Driver to assign
            copied_shared_files: Set tracking shared files already copied

        Returns:
            Relative path to isolated vehicle

        Raises:
            FileNotFoundError: If original vehicle file doesn't exist
            ValueError: If vehicle cannot be parsed
            IOError: If copying or modification fails
        """
        # Resolve original vehicle path
        original_path = self.vehicles_dir / vehicle_path
        if not original_path.exists():
            raise FileNotFoundError(f"Vehicle not found: {original_path}")

        # Validate that we can parse the vehicle (early validation)
        try:
            vehicle = self.veh_parser.parse_file(original_path)
            if vehicle is None:
                raise ValueError(f"Failed to parse vehicle: {original_path}")
        except Exception as e:
            raise ValueError(f"Cannot parse vehicle {original_path}: {e}")

        # Determine new path (preserve structure)
        # Example: RHEZ/2005RHEZ/GT3/TEAM_YELLOW/YEL_09.veh
        # becomes: RFTOOL_MyChamp/2005RHEZ/GT3/TEAM_YELLOW/YEL_09.veh
        #
        # Strategy:
        # - If path has multiple parts, skip the first part (original mod folder)
        # - Keep the rest of the structure
        # - If path has only one part (file in root), just prefix it
        path_parts = Path(vehicle_path).parts

        if len(path_parts) > 1:
            # Multi-level path: skip first component (mod folder)
            new_relative_parts = [champ_prefix] + list(path_parts[1:])
        else:
            # Single-level path: just add prefix directory
            new_relative_parts = [champ_prefix, path_parts[0]]

        # Generate vehicle prefix (e.g., "TC" for "TestChampionship")
        vehicle_prefix = self._generate_vehicle_prefix(championship_name)

        # Rename the .veh file with prefix to avoid conflicts
        # Example: GRN_08.veh -> TC_GRN_08.veh
        original_veh_name = Path(vehicle_path).name
        new_veh_name = f"{vehicle_prefix}_{original_veh_name}"

        # Update the path with new filename
        new_relative_parts_with_rename = list(new_relative_parts[:-1]) + [new_veh_name]
        new_relative_path = Path(*new_relative_parts_with_rename)
        new_absolute_path = self.vehicles_dir / new_relative_path

        # Create directory structure
        try:
            new_absolute_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise IOError(f"Failed to create directory {new_absolute_path.parent}: {e}")

        # Copy vehicle file with new name
        try:
            shutil.copy2(original_path, new_absolute_path)
        except Exception as e:
            raise IOError(f"Failed to copy vehicle {original_path} to {new_absolute_path}: {e}")

        # Copy vehicle-specific assets (textures, etc.)
        # This function handles its own errors with warnings
        try:
            self._copy_vehicle_assets(
                original_path.parent,
                new_absolute_path.parent,
                original_veh_name,
                vehicle_prefix
            )
        except Exception as e:
            print(f"Warning: Error copying local assets for {vehicle_path}: {e}")

        # Copy shared assets (HDV, SFX, GEN, etc.)
        # Uses the vehicle object we already parsed for validation
        try:
            self._copy_shared_assets(
                vehicle,
                original_path,
                new_absolute_path,
                copied_shared_files
            )
        except Exception as e:
            print(f"Warning: Error copying shared assets for {vehicle_path}: {e}")

        # Modify the copied vehicle
        # This can raise FileNotFoundError, ValueError, or IOError
        self._modify_vehicle_file(
            str(new_absolute_path),
            championship_name,
            driver_name,
            vehicle_prefix
        )

        # Return relative path (with forward slashes for consistency)
        return str(new_relative_path).replace('\\', '/')

    def _copy_vehicle_assets(
        self,
        source_dir: Path,
        dest_dir: Path,
        original_veh_name: str,
        vehicle_prefix: str
    ) -> None:
        """
        Copy vehicle-specific assets (textures, etc.) from source to destination.

        These are files in the same directory as the .veh file.
        Assets are renamed with the vehicle prefix to avoid conflicts.

        Args:
            source_dir: Source directory (original vehicle folder)
            dest_dir: Destination directory (isolated vehicle folder)
            original_veh_name: Original .veh filename (e.g., "GRN_08.veh")
            vehicle_prefix: Prefix to add to filenames (e.g., "TC")
        """
        # Get base name without extension for matching related files
        veh_base = Path(original_veh_name).stem  # e.g., "GRN_08"

        # Extensions to rename (vehicle-specific files)
        rename_extensions = ['.dds', '.tga', '.bmp', '.txt']

        # Extensions to copy without renaming (shared files)
        copy_extensions = ['.gmt', '.mas', '.gen']

        # Track copied files by lowercase name to avoid duplicates on case-insensitive filesystems
        copied_files = set()

        # Copy all files in the directory
        for asset_file in source_dir.iterdir():
            if not asset_file.is_file():
                continue

            file_key = asset_file.name.lower()
            if file_key in copied_files:
                continue  # Already copied

            ext_lower = asset_file.suffix.lower()

            # Skip .veh files (they are copied separately with renaming)
            if ext_lower == '.veh':
                continue

            # Determine if this file should be renamed
            should_rename = False
            if ext_lower in rename_extensions:
                # Check if filename starts with vehicle base name
                # Example: GRN_08.DDS, GRN_08.txt -> rename
                #          other.txt -> don't rename
                if asset_file.stem.upper() == veh_base.upper():
                    should_rename = True

            # Determine destination filename
            if should_rename:
                # Rename: GRN_08.DDS -> TC_GRN_08.DDS
                new_name = f"{vehicle_prefix}_{asset_file.name}"
            else:
                # Keep original name
                new_name = asset_file.name

            dest_file = dest_dir / new_name

            # Copy file
            try:
                if not dest_file.exists():
                    shutil.copy2(asset_file, dest_file)
                    copied_files.add(file_key)
            except Exception as e:
                print(f"Warning: Failed to copy {asset_file.name}: {e}")

    def _copy_shared_assets(
        self,
        vehicle: Vehicle,
        original_veh_path: Path,
        isolated_veh_path: Path,
        copied_shared_files: set
    ) -> None:
        """
        Copy shared assets referenced by the vehicle (HDV, SFX, GEN, etc.).

        These files are typically in parent directories and shared between vehicles.
        Also copies all indirect dependencies (.tbc, .ini) from parent directories.

        Args:
            vehicle: Parsed Vehicle object
            original_veh_path: Path to original .veh file
            isolated_veh_path: Path to isolated .veh file
            copied_shared_files: Set to track already copied files (to avoid duplicates)
        """
        # List of referenced files from vehicle config
        references = [
            ('HDVehicle', vehicle.config.hdvehicle),
            ('Graphics', vehicle.config.graphics),
            ('Spinner', vehicle.config.spinner),
            ('Sounds', vehicle.config.sounds),
            ('Cameras', vehicle.config.cameras),
            ('Upgrades', vehicle.config.upgrades),
            ('HeadPhysics', vehicle.config.head_physics),
            ('Cockpit', vehicle.config.cockpit),
        ]

        for ref_name, ref_value in references:
            if not ref_value:
                continue  # Skip empty references

            # Normalize path separators
            ref_value = ref_value.replace('/', '\\')
            ref_path = Path(ref_value)

            # Skip absolute paths (shouldn't happen, but be safe)
            if ref_path.is_absolute():
                continue

            # Resolve the reference by searching up from the vehicle directory
            source_file = self._resolve_reference(original_veh_path.parent, ref_path)

            if source_file and source_file.exists():
                # Use lowercase for duplicate detection (case-insensitive filesystems)
                file_key = str(source_file).lower()

                if file_key not in copied_shared_files:
                    # Calculate relative position from Vehicles directory
                    try:
                        rel_to_vehicles = source_file.relative_to(self.vehicles_dir)
                    except ValueError:
                        # File is outside Vehicles directory (shouldn't happen)
                        print(f"Warning: Referenced file outside Vehicles dir: {source_file}")
                        continue

                    # Get the original mod folder name (first component in path)
                    original_mod_folder = rel_to_vehicles.parts[0]

                    # Get the isolated mod folder name (RFTOOL_XXX)
                    isolated_mod_folder = isolated_veh_path.relative_to(self.vehicles_dir).parts[0]

                    # Preserve EXACT relative structure by replacing only the root folder
                    # Example: Rhez/Rhez.hdv -> RFTOOL_MyChamp/Rhez.hdv
                    #          Rhez/2005Rhez/foo.sfx -> RFTOOL_MyChamp/2005Rhez/foo.sfx
                    dest_parts = [isolated_mod_folder] + list(rel_to_vehicles.parts[1:])
                    dest_file = self.vehicles_dir / Path(*dest_parts)

                    # Create parent directory
                    try:
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        print(f"Warning: Failed to create directory for {ref_name}: {e}")
                        continue

                    # Copy file
                    try:
                        if not dest_file.exists():
                            shutil.copy2(source_file, dest_file)
                            copied_shared_files.add(file_key)
                    except Exception as e:
                        print(f"Warning: Failed to copy {ref_name} ({source_file.name}): {e}")
            else:
                print(f"Warning: Referenced file not found: {ref_name}={ref_value}")

        # ADDITIONAL: Copy all indirect dependencies from parent directories
        # (TBC, INI files referenced by HDV but not directly in VEH)
        self._copy_indirect_dependencies(
            original_veh_path,
            isolated_veh_path,
            copied_shared_files
        )

    def _resolve_reference(self, start_dir: Path, ref_path: Path) -> Optional[Path]:
        """
        Resolve a file reference by searching up from the start directory.

        Args:
            start_dir: Directory to start searching from (vehicle folder)
            ref_path: Reference path to resolve (e.g., "Rhez.hdv")

        Returns:
            Resolved absolute path, or None if not found
        """
        # If reference has multiple parts (e.g., "subdir/file.hdv"), resolve from Vehicles root
        if len(ref_path.parts) > 1:
            candidate = self.vehicles_dir / ref_path
            if candidate.exists():
                return candidate
            return None

        # Single filename: search up the directory tree
        current = start_dir
        vehicles_root = self.vehicles_dir

        while True:
            candidate = current / ref_path
            if candidate.exists():
                return candidate

            # Stop at Vehicles root
            try:
                if current.resolve() == vehicles_root.resolve():
                    break
            except Exception:
                if str(current) == str(vehicles_root):
                    break

            # Move up one directory
            parent = current.parent
            if parent == current:  # Reached filesystem root
                break
            current = parent

        return None

    def _modify_vehicle_file(
        self,
        vehicle_path: str,
        championship_name: str,
        driver_name: str,
        vehicle_prefix: str
    ) -> None:
        """
        Modify a vehicle file to update Classes, Driver, and Description.

        Uses the VEH parser to validate the file structure before modification.
        Preserves all comments, formatting, and order of the original file.

        Args:
            vehicle_path: Path to vehicle file to modify
            championship_name: Championship name (for Classes)
            driver_name: Driver name to set
            vehicle_prefix: Short prefix to add to Description (e.g., "TC")

        Raises:
            FileNotFoundError: If vehicle file doesn't exist
            ValueError: If vehicle file is invalid or cannot be parsed
            IOError: If file cannot be read or written
        """
        vehicle_path_obj = Path(vehicle_path)

        # Validate that file exists
        if not vehicle_path_obj.exists():
            raise FileNotFoundError(f"Vehicle file not found: {vehicle_path}")

        # Parse the vehicle file to validate structure
        try:
            vehicle = self.veh_parser.parse_file(vehicle_path)
            if vehicle is None:
                raise ValueError(f"Failed to parse vehicle file: {vehicle_path}")
        except Exception as e:
            raise ValueError(f"Invalid vehicle file {vehicle_path}: {e}")

        # Read file lines (preserving original structure)
        try:
            with open(vehicle_path, 'r', encoding='windows-1252') as f:
                lines = f.readlines()
        except Exception as e:
            raise IOError(f"Failed to read vehicle file {vehicle_path}: {e}")

        # Modify lines
        modified_lines = []
        classes_modified = False
        driver_modified = False
        description_modified = False

        for line in lines:
            stripped = line.strip()

            # Check for any Livery line (DefaultLivery, PitCrewLivery, TrackLivery)
            if any(stripped.startswith(f"{prefix}=") or stripped.startswith(f"{prefix} =")
                   for prefix in ["DefaultLivery", "PitCrewLivery", "TrackLivery"]):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    # Get field name
                    field_name = parts[0].strip()

                    # Get existing value (remove quotes and comments)
                    existing_value = parts[1].split('//')[0].strip().strip('"')

                    # For TrackLivery, format is "TRACK_NAME, LIVERY_FILE"
                    if field_name == "TrackLivery" and ',' in existing_value:
                        track_name, livery_file = existing_value.split(',', 1)
                        livery_file = livery_file.strip()
                        livery_path = Path(livery_file)
                        new_livery = f"{vehicle_prefix}_{livery_path.name}"
                        new_value = f"{track_name.strip()}, {new_livery}"
                    else:
                        # DefaultLivery or PitCrewLivery
                        # Example: GRN_08.DDS -> TC_GRN_08.DDS
                        livery_path = Path(existing_value)
                        new_value = f"{vehicle_prefix}_{livery_path.name}"

                    # Preserve indentation
                    indent = line[:len(line) - len(line.lstrip())]
                    modified_lines.append(f'{indent}{field_name}="{new_value}"\n')
                else:
                    modified_lines.append(line)

            # Check for Classes line (with or without spaces around =)
            elif stripped.startswith("Classes=") or stripped.startswith("Classes ="):
                # Extract current classes
                parts = line.split('=', 1)
                if len(parts) == 2:
                    # Get existing classes (remove quotes and comments)
                    existing_classes = parts[1].split('//')[0].strip().strip('"')
                    class_list = [c.strip() for c in existing_classes.split() if c.strip()]

                    # Keep only ONE base class (first non-specific class)
                    # Filter out year numbers, specific mod names, and AI_ONLY
                    base_class = None
                    for cls in class_list:
                        # Skip numbers (like "2005"), AI_ONLY, and mod-specific names
                        if not cls.isdigit() and cls != "AI_ONLY" and cls not in ["Rhez", "ZR", "Howston", "Hammer"]:
                            base_class = cls
                            break

                    # Build new class list: championship name + base class (if found)
                    if base_class:
                        new_classes = f"{championship_name} {base_class}"
                    else:
                        # Fallback: just championship name (but this might cause issues)
                        new_classes = championship_name

                    # Reconstruct line (preserve indentation)
                    indent = line[:len(line) - len(line.lstrip())]
                    modified_lines.append(f'{indent}Classes="{new_classes}"\n')
                    classes_modified = True
                else:
                    modified_lines.append(line)

            # Check for Driver line (with or without spaces around =)
            elif stripped.startswith("Driver=") or stripped.startswith("Driver ="):
                # Preserve indentation
                indent = line[:len(line) - len(line.lstrip())]
                modified_lines.append(f'{indent}Driver="{driver_name}"\n')
                driver_modified = True

            # Check for Description line (add prefix to make it unique)
            elif stripped.startswith("Description=") or stripped.startswith("Description ="):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    # Get existing description (remove quotes and comments)
                    existing_desc = parts[1].split('//')[0].strip().strip('"')

                    # Add prefix if not already present
                    if not existing_desc.startswith(vehicle_prefix):
                        new_desc = f"{vehicle_prefix} {existing_desc}"
                    else:
                        new_desc = existing_desc

                    # Preserve indentation
                    indent = line[:len(line) - len(line.lstrip())]
                    modified_lines.append(f'{indent}Description="{new_desc}"\n')
                    description_modified = True
                else:
                    modified_lines.append(line)

            else:
                modified_lines.append(line)

        # Verify that we actually modified the required fields
        if not classes_modified:
            print(f"Warning: Classes field not found in {vehicle_path}")
        if not driver_modified:
            print(f"Warning: Driver field not found in {vehicle_path}")

        # Write back
        try:
            with open(vehicle_path, 'w', encoding='windows-1252') as f:
                f.writelines(modified_lines)
        except Exception as e:
            raise IOError(f"Failed to write vehicle file {vehicle_path}: {e}")

    def _copy_indirect_dependencies(
        self,
        original_veh_path: Path,
        isolated_veh_path: Path,
        copied_shared_files: set
    ) -> None:
        """
        Copy indirect dependencies (TBC, INI, PM files) from parent directories.

        These are files referenced by HDV/GEN files but not directly in the VEH.
        Examples: tire files (.tbc), engine.ini, gears.ini, suspension (.pm)

        Args:
            original_veh_path: Path to original .veh file
            isolated_veh_path: Path to isolated .veh file
            copied_shared_files: Set to track already copied files (to avoid duplicates)
        """
        # Extensions to copy (indirect dependencies)
        indirect_extensions = ['.tbc', '.ini', '.mas', '.pm']

        # Get the original vehicle's parent directory tree
        # We'll search up to 2 levels up from the vehicle file
        original_dir = original_veh_path.parent

        # Get the isolated mod folder name
        isolated_mod_folder = isolated_veh_path.relative_to(self.vehicles_dir).parts[0]

        # Search parent directories (up to 2 levels)
        search_dirs = [
            original_dir,                    # Same directory as .veh
            original_dir.parent,              # 1 level up (e.g., GT3/)
            original_dir.parent.parent,       # 2 levels up (e.g., 2005RHEZ/)
        ]

        for search_dir in search_dirs:
            # Verify we're still within Vehicles directory
            try:
                if not search_dir.is_relative_to(self.vehicles_dir):
                    continue
            except (ValueError, AttributeError):
                # Python < 3.9 doesn't have is_relative_to
                try:
                    search_dir.relative_to(self.vehicles_dir)
                except ValueError:
                    continue

            if not search_dir.exists() or not search_dir.is_dir():
                continue

            # Copy all files with target extensions
            for file_path in search_dir.iterdir():
                if not file_path.is_file():
                    continue

                ext_lower = file_path.suffix.lower()
                if ext_lower not in indirect_extensions:
                    continue

                # Check if already copied
                file_key = str(file_path).lower()
                if file_key in copied_shared_files:
                    continue

                # Calculate destination path (preserve structure)
                try:
                    rel_to_vehicles = file_path.relative_to(self.vehicles_dir)
                except ValueError:
                    continue

                # Replace root folder with isolated folder
                original_mod_folder = rel_to_vehicles.parts[0]
                dest_parts = [isolated_mod_folder] + list(rel_to_vehicles.parts[1:])
                dest_file = self.vehicles_dir / Path(*dest_parts)

                # Create parent directory
                try:
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    print(f"Warning: Failed to create directory for {file_path.name}: {e}")
                    continue

                # Copy file
                try:
                    if not dest_file.exists():
                        shutil.copy2(file_path, dest_file)
                        copied_shared_files.add(file_key)
                        print(f"  [Indirect] Copied: {file_path.name}")
                except Exception as e:
                    print(f"Warning: Failed to copy indirect dependency {file_path.name}: {e}")

    def cleanup_championship_vehicles(self, championship_name: str) -> None:
        """
        Remove isolated vehicles for a championship.

        Args:
            championship_name: Name of championship to clean up

        Raises:
            ValueError: If championship name is empty
            IOError: If deletion fails
        """
        if not championship_name:
            raise ValueError("Championship name cannot be empty")

        champ_prefix = f"M_{championship_name}"
        champ_dir = self.vehicles_dir / champ_prefix

        if champ_dir.exists():
            try:
                shutil.rmtree(champ_dir)
                print(f"Cleaned up isolated vehicles for championship: {championship_name}")
            except Exception as e:
                raise IOError(f"Failed to delete championship directory {champ_dir}: {e}")
        else:
            print(f"No isolated vehicles found for championship: {championship_name}")

    def list_isolated_championships(self) -> List[str]:
        """
        List all isolated championships (directories starting with M_).

        Returns:
            List of championship names (without M_ prefix)
        """
        championships = []

        for item in self.vehicles_dir.iterdir():
            if item.is_dir() and item.name.startswith("M_"):
                champ_name = item.name.replace("M_", "")
                championships.append(champ_name)

        return championships

    def copy_all_dependencies(
        self,
        vehicle_path: Path,
        target_dir: Path,
        vehicles_root: Path
    ) -> Set[Path]:
        """
        Copy ALL dependencies for a vehicle to target directory.

        Uses the DependencyCollector to recursively find and copy all files
        needed by a vehicle (HDV, GEN, INI, MAS, assets, etc.).

        Args:
            vehicle_path: Path to the source .veh file
            target_dir: Target directory (championship root)
            vehicles_root: Root Vehicles directory

        Returns:
            Set of paths that were copied

        Raises:
            IOError: If copying fails
        """
        # Collect all dependencies
        all_deps = self.dependency_collector.collect_all_dependencies(vehicle_path, vehicles_root)

        copied_files = set()

        for dep_path in all_deps:
            # Compute relative path from vehicles_root
            try:
                rel_path = dep_path.relative_to(vehicles_root)
            except ValueError:
                # File is outside vehicles_root (shouldn't happen, but handle gracefully)
                print(f"Warning: Dependency outside vehicles root: {dep_path}")
                continue

            # Compute target path
            target_path = target_dir / rel_path

            # Skip if already copied
            if target_path.exists():
                continue

            # Create parent directories
            try:
                target_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Warning: Failed to create directory {target_path.parent}: {e}")
                continue

            # Copy file
            try:
                shutil.copy2(dep_path, target_path)
                copied_files.add(target_path)
            except Exception as e:
                print(f"Warning: Failed to copy {dep_path} to {target_path}: {e}")

        return copied_files
