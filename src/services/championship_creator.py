"""
Service for creating custom championships.

Orchestrates RFM generation and vehicle isolation.
"""

from pathlib import Path
from typing import List, Dict, Optional

from ..models.rfm import RFMod, Season, DefaultScoring, SeasonScoringInfo, PitGroup
from ..generators.rfm_generator import generate_rfm
from .vehicle_isolation_service import VehicleIsolationService


class ChampionshipCreator:
    """Service for creating custom championships."""

    def __init__(self, rfactor_path: str):
        """
        Initialize service.

        Args:
            rfactor_path: Path to rFactor installation

        Raises:
            FileNotFoundError: If rFactor path doesn't exist
        """
        self.rfactor_path = Path(rfactor_path)

        # Validate rFactor path exists
        if not self.rfactor_path.exists():
            raise FileNotFoundError(f"rFactor path not found: {rfactor_path}")

        self.rfm_dir = self.rfactor_path / "rFm"
        self.isolation_service = VehicleIsolationService(rfactor_path)

        # Create rFm directory if it doesn't exist
        self.rfm_dir.mkdir(parents=True, exist_ok=True)

    def create_championship(
        self,
        championship_name: str,
        vehicle_assignments: List[Dict[str, str]],
        tracks: List[str],
        options: Optional[Dict] = None
    ) -> str:
        """
        Create a complete custom championship.

        This method:
        1. Isolates selected vehicles with driver assignments
        2. Generates the RFM file
        3. Returns the path to the created RFM file

        Args:
            championship_name: Name of the championship (unique identifier)
            vehicle_assignments: List of dicts with keys:
                - 'vehicle_path': Relative path to original .veh
                - 'driver_name': Name of driver to assign
            tracks: List of track names (scene order)
            options: Optional dict with championship settings:
                - 'full_name': Full championship name (default: championship_name)
                - 'max_opponents': Max opponents (default: based on vehicle count)
                - 'default_scoring': DefaultScoring object
                - 'season_scoring': SeasonScoringInfo object
                - 'pit_groups': List of PitGroup objects

        Returns:
            Path to created RFM file

        Raises:
            ValueError: If inputs are invalid
            FileNotFoundError: If vehicles not found
            IOError: If isolation or file creation fails

        Example:
            >>> creator = ChampionshipCreator("/path/to/rFactor")
            >>> assignments = [
            ...     {'vehicle_path': 'RHEZ/.../YEL_09.veh', 'driver_name': 'John Doe'},
            ...     {'vehicle_path': 'RHEZ/.../BLU_07.veh', 'driver_name': 'Jane Smith'}
            ... ]
            >>> tracks = ['Mills_Short', 'Toban_Long', 'Joesville_Speedway']
            >>> rfm_path = creator.create_championship(
            ...     "MyChamp2025",
            ...     assignments,
            ...     tracks
            ... )
        """
        options = options or {}

        # Validate inputs
        if not championship_name:
            raise ValueError("Championship name is required")
        if not championship_name.replace('_', '').isalnum():
            raise ValueError("Championship name must be alphanumeric (underscores allowed)")

        # Validate name length for multiplayer compatibility
        # RFM filename limit: 19 characters (excluding .rfm extension)
        rfm_filename = f"M_{championship_name}"
        if len(rfm_filename) > 19:
            raise ValueError(
                f"Championship name too long: '{rfm_filename}' ({len(rfm_filename)} chars). "
                f"Maximum allowed: 19 characters. "
                f"Please use a shorter name (max {19 - len('M_')} characters)."
            )

        if not vehicle_assignments:
            raise ValueError("At least one vehicle assignment is required")
        if not tracks:
            raise ValueError("At least one track is required")

        # Check if championship already exists
        rfm_filename = f"M_{championship_name}.rfm"
        rfm_path = self.rfm_dir / rfm_filename
        if rfm_path.exists():
            raise ValueError(f"Championship '{championship_name}' already exists at {rfm_path}")

        # Step 1: Isolate vehicles
        print(f"Isolating {len(vehicle_assignments)} vehicles...")
        try:
            isolated_paths = self.isolation_service.isolate_vehicles(
                championship_name,
                vehicle_assignments
            )
        except (ValueError, FileNotFoundError, IOError) as e:
            raise IOError(f"Failed to isolate vehicles: {e}")

        # Verify we got at least one isolated vehicle
        if not isolated_paths:
            raise IOError("No vehicles were successfully isolated")

        # Step 2: Create RFM
        print(f"Creating RFM file...")
        try:
            rfm = self._create_rfm(
                championship_name,
                tracks,
                len(isolated_paths),  # Use actual isolated count, not requested count
                options
            )
        except Exception as e:
            raise ValueError(f"Failed to create RFM structure: {e}")

        # Step 3: Generate RFM file
        try:
            generate_rfm(rfm, str(rfm_path))
        except Exception as e:
            # Clean up isolated vehicles if RFM generation fails
            try:
                self.isolation_service.cleanup_championship_vehicles(championship_name)
            except:
                pass  # Ignore cleanup errors
            raise IOError(f"Failed to generate RFM file: {e}")

        print(f"Championship created successfully: {rfm_path}")
        return str(rfm_path)

    def _create_rfm(
        self,
        championship_name: str,
        tracks: List[str],
        num_vehicles: int,
        options: Dict
    ) -> RFMod:
        """
        Create RFMod object for the championship.

        Args:
            championship_name: Championship name
            tracks: List of track names
            num_vehicles: Number of vehicles in championship
            options: Championship options

        Returns:
            RFMod object
        """
        # Create vehicle filter (same as championship name for isolation)
        vehicle_filter = championship_name

        # Determine max opponents (num_vehicles - 1 for player)
        max_opponents = num_vehicles - 1
        if max_opponents < 1:
            max_opponents = 1

        # Get full name
        full_name = options.get('full_name', championship_name)

        # Validate season name length for multiplayer compatibility
        season_name = f"{full_name} Season"
        if len(season_name) > 19:
            # Try abbreviated version
            season_name = f"{full_name} S1"
            if len(season_name) > 19:
                # Truncate full_name to fit
                max_name_length = 19 - len(" S1")
                season_name = f"{full_name[:max_name_length]} S1"

        # Create RFMod
        rfm = RFMod(
            mod_name=full_name,
            vehicle_filter=vehicle_filter,
            track_filter="*",
            max_opponents=max_opponents,
            min_championship_opponents=min(3, max_opponents)
        )

        # Create season
        season = Season(
            name=season_name,
            vehicle_filter=vehicle_filter,
            scene_order=tracks,
            min_championship_opponents=min(3, max_opponents)
        )
        rfm.add_season(season)

        # Set scoring if provided
        if 'default_scoring' in options:
            rfm.default_scoring = options['default_scoring']

        if 'season_scoring' in options:
            rfm.season_scoring_info = options['season_scoring']

        # Set pit groups if provided
        if 'pit_groups' in options:
            rfm.pit_group_order = options['pit_groups']
        else:
            # Generate default pit groups
            rfm.pit_group_order = self._generate_default_pit_groups(num_vehicles)

        # Set scene order (global track list)
        rfm.scene_order = tracks

        return rfm

    def _generate_default_pit_groups(self, num_vehicles: int) -> List[PitGroup]:
        """
        Generate default pit groups (1 vehicle per group).

        Args:
            num_vehicles: Number of vehicles

        Returns:
            List of PitGroup objects
        """
        pit_groups = []
        for i in range(num_vehicles):
            pit_groups.append(PitGroup(1, f"Group{i + 1}"))
        return pit_groups

    def delete_championship(self, championship_name: str) -> None:
        """
        Delete a custom championship (RFM and isolated vehicles).

        Args:
            championship_name: Name of championship to delete

        Raises:
            ValueError: If championship name is empty
            IOError: If deletion fails
        """
        if not championship_name:
            raise ValueError("Championship name is required")

        # Delete RFM file
        rfm_filename = f"M_{championship_name}.rfm"
        rfm_path = self.rfm_dir / rfm_filename

        rfm_deleted = False
        if rfm_path.exists():
            try:
                rfm_path.unlink()
                print(f"Deleted RFM file: {rfm_path}")
                rfm_deleted = True
            except Exception as e:
                raise IOError(f"Failed to delete RFM file {rfm_path}: {e}")

        # Delete isolated vehicles
        try:
            self.isolation_service.cleanup_championship_vehicles(championship_name)
        except Exception as e:
            if rfm_deleted:
                print(f"Warning: RFM deleted but vehicles cleanup failed: {e}")
            else:
                raise IOError(f"Failed to cleanup vehicles: {e}")

        if not rfm_deleted:
            print(f"Championship '{championship_name}' not found")

    def list_custom_championships(self) -> List[str]:
        """
        List all custom championships created by this tool.

        Returns:
            List of championship names
        """
        championships = []

        # List RFM files
        if self.rfm_dir.exists():
            for rfm_file in self.rfm_dir.glob("M_*.rfm"):
                champ_name = rfm_file.stem.replace("M_", "")
                championships.append(champ_name)

        return championships

    def validate_championship_name(self, name: str) -> bool:
        """
        Validate if a championship name is available.

        Args:
            name: Championship name to check

        Returns:
            True if name is available, False otherwise
        """
        rfm_filename = f"RFTOOL_{name}.rfm"
        rfm_path = self.rfm_dir / rfm_filename

        return not rfm_path.exists()
