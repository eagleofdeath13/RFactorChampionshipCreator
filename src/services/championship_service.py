"""
Service for managing rFactor Championships.

Provides methods to list, get, create, and manage championships.
"""

from pathlib import Path
from typing import List, Optional

from ..models.championship import Championship
from ..models.rfm import RFMod
from ..parsers.cch_parser import CCHParser
from ..parsers.rfm_parser import RFMParser
from ..generators.cch_generator import CCHGenerator
from ..utils.file_utils import find_files_by_extension
from ..utils.rfactor_validator import RFactorValidator


class ChampionshipService:
    """Service for managing championships."""

    def __init__(self, rfactor_path: str, player_name: Optional[str] = None, validate: bool = True):
        """
        Initialize the ChampionshipService.

        Args:
            rfactor_path: Path to the rFactor installation directory
            player_name: Name of the player profile (if None, auto-detects or creates default)
            validate: Whether to validate the rFactor installation (default: True)

        Raises:
            ValueError: If validate=True and the path is invalid
        """
        self.rfactor_path = Path(rfactor_path)

        # Validate rFactor installation if requested
        if validate:
            RFactorValidator.validate_or_raise(str(self.rfactor_path))

        # Auto-detect or create player if not specified
        if player_name is None:
            player_name = self._get_or_create_default_player()

        self.player_name = player_name
        self.userdata_dir = self.rfactor_path / "UserData" / player_name
        self.rfm_dir = self.rfactor_path / "rFm"

        if not self.userdata_dir.exists():
            # Create player directory if it doesn't exist
            self.userdata_dir.mkdir(parents=True, exist_ok=True)

    def _get_or_create_default_player(self) -> str:
        """
        Get the first available player or create a default one.

        Returns:
            Player profile name
        """
        userdata_path = self.rfactor_path / "UserData"

        # If UserData doesn't exist, create it with DefaultPlayer
        if not userdata_path.exists():
            userdata_path.mkdir(parents=True, exist_ok=True)
            return "DefaultPlayer"

        # List existing player directories
        player_dirs = [d for d in userdata_path.iterdir() if d.is_dir()]

        # If players exist, return the first one
        if player_dirs:
            return player_dirs[0].name

        # No players found, create DefaultPlayer
        return "DefaultPlayer"

    def list_all(self) -> List[str]:
        """
        List all available championships for the player.

        Returns:
            List of championship filenames (without .cch extension)
        """
        if not self.userdata_dir.exists():
            return []

        cch_files = find_files_by_extension(str(self.userdata_dir), '.cch', recursive=False)
        return sorted([f.stem for f in cch_files])

    def get(self, name: str) -> Optional[Championship]:
        """
        Get a championship by name.

        Args:
            name: Name of the championship file (without .cch extension)

        Returns:
            Championship object or None if not found
        """
        # Ensure .cch extension
        if not name.endswith('.cch'):
            name = f"{name}.cch"

        filepath = self.userdata_dir / name

        if not filepath.exists():
            return None

        try:
            return CCHParser.parse_file(str(filepath))
        except Exception:
            return None

    def exists(self, name: str) -> bool:
        """
        Check if a championship exists.

        Args:
            name: Name of the championship

        Returns:
            True if championship exists, False otherwise
        """
        return self.get(name) is not None

    def get_championship_info(self, name: str) -> Optional[dict]:
        """
        Get basic info about a championship without loading it fully.

        Args:
            name: Name of the championship

        Returns:
            Dictionary with basic info or None if not found
        """
        championship = self.get(name)
        if not championship:
            return None

        return {
            'name': championship.season.name,
            'status': championship.season.season_status,
            'player': championship.player.name if championship.player else 'Unknown',
            'opponents': len(championship.opponents),
            'current_race': championship.season.current_race,
            'player_points': championship.player.season_points if championship.player else 0,
            'player_position': championship.player.points_position if championship.player else 0,
        }

    def list_rfm_files(self) -> List[str]:
        """
        List all RFM files (championship definitions).

        Returns:
            List of RFM filenames (without .rfm extension)
        """
        if not self.rfm_dir.exists():
            return []

        rfm_files = find_files_by_extension(str(self.rfm_dir), '.rfm', recursive=False)
        return sorted([f.stem for f in rfm_files])

    def get_rfm(self, name: str) -> Optional[RFMod]:
        """
        Get a complete RFM championship definition.

        Args:
            name: Name of the RFM file (without .rfm extension)

        Returns:
            RFMod object or None if not found
        """
        # Ensure .rfm extension
        if not name.endswith('.rfm'):
            name = f"{name}.rfm"

        filepath = self.rfm_dir / name

        if not filepath.exists():
            return None

        try:
            parser = RFMParser(str(filepath))
            return parser.parse()
        except Exception:
            return None

    def get_rfm_info(self, name: str) -> Optional[dict]:
        """
        Get basic info about an RFM championship.

        Args:
            name: Name of the RFM file (without .rfm extension)

        Returns:
            Dictionary with basic RFM info or None if not found
        """
        # Ensure .rfm extension
        if not name.endswith('.rfm'):
            name = f"{name}.rfm"

        filepath = self.rfm_dir / name

        if not filepath.exists():
            return None

        try:
            parser = RFMParser(str(filepath))
            rfm = parser.parse()

            # Check if this is a custom championship (M_)
            is_custom = name.startswith('M_')

            # Count number of tracks in first season
            num_tracks = 0
            if rfm.seasons and len(rfm.seasons) > 0:
                num_tracks = len(rfm.seasons[0].scene_order)

            return {
                'name': rfm.mod_name or rfm.seasons[0].name if rfm.seasons else 'Unknown',
                'status': -1,  # RFM files don't have status (not started)
                'player': 'N/A',  # RFM files don't have player info
                'opponents': 0,  # Will be determined when championship starts
                'current_race': 0,
                'player_points': 0,
                'is_rfm': True,
                'is_custom': is_custom,
                'num_tracks': num_tracks,
            }
        except Exception:
            return None

    def list_all_with_info(self) -> List[dict]:
        """
        List all championships with their basic information.
        Includes both RFM files (championship definitions) and CCH files (player progress).
        RFM files are listed first, followed by CCH files.

        Returns:
            List of dictionaries with championship info
        """
        championships = []

        # First, add all RFM files
        for name in self.list_rfm_files():
            info = self.get_rfm_info(name)
            if info:
                info['filename'] = name
                info['type'] = 'RFM'
                championships.append(info)

        # Then, add all CCH files (player progress)
        for name in self.list_all():
            info = self.get_championship_info(name)
            if info:
                info['filename'] = name
                info['type'] = 'CCH'
                info['is_rfm'] = False
                championships.append(info)

        return championships

    def create(self, championship: Championship, filename: str) -> None:
        """
        Create a new championship.

        Args:
            championship: Championship object to create
            filename: Filename for the championship (without .cch extension)

        Raises:
            FileExistsError: If championship already exists
        """
        # Ensure .cch extension
        if not filename.endswith('.cch'):
            filename = f"{filename}.cch"

        filepath = self.userdata_dir / filename

        if filepath.exists():
            raise FileExistsError(f"Championship already exists: {filename}")

        CCHGenerator.generate(championship, str(filepath))

    def update(self, championship: Championship, filename: str) -> None:
        """
        Update an existing championship.

        Args:
            championship: Championship object to save
            filename: Filename of the championship (without .cch extension)

        Raises:
            FileNotFoundError: If championship doesn't exist
        """
        # Ensure .cch extension
        if not filename.endswith('.cch'):
            filename = f"{filename}.cch"

        filepath = self.userdata_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Championship not found: {filename}")

        CCHGenerator.generate(championship, str(filepath))

    def save(self, championship: Championship, filename: str) -> None:
        """
        Save a championship (create or update).

        Args:
            championship: Championship object to save
            filename: Filename for the championship (without .cch extension)
        """
        # Ensure .cch extension
        if not filename.endswith('.cch'):
            filename = f"{filename}.cch"

        filepath = self.userdata_dir / filename

        CCHGenerator.generate(championship, str(filepath))

    def delete(self, filename: str) -> None:
        """
        Delete a championship.

        Args:
            filename: Name of the championship to delete (without .cch)

        Raises:
            FileNotFoundError: If championship doesn't exist
        """
        # Ensure .cch extension
        if not filename.endswith('.cch'):
            filename = f"{filename}.cch"

        filepath = self.userdata_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Championship not found: {filename}")

        filepath.unlink()

    def duplicate(self, source_filename: str, new_filename: str) -> Championship:
        """
        Duplicate an existing championship.

        Args:
            source_filename: Name of championship to duplicate
            new_filename: Name for the new championship

        Returns:
            The duplicated Championship object

        Raises:
            FileNotFoundError: If source doesn't exist
            FileExistsError: If new_filename already exists
        """
        # Load source
        championship = self.get(source_filename)
        if not championship:
            raise FileNotFoundError(f"Championship not found: {source_filename}")

        # Reset some fields for the duplicate
        championship.season.season_status = 0  # Not started
        championship.season.current_race = 0
        championship.season.race_session = 0
        championship.season.race_over = 0

        # Reset player stats
        if championship.player:
            championship.player.season_points = 0
            championship.player.points_position = 0
            championship.player.poles_taken = 0

        # Reset opponent stats
        for opponent in championship.opponents:
            opponent.season_points = 0
            opponent.points_position = 0
            opponent.poles_taken = 0

        # Save as new file
        self.create(championship, new_filename)

        return championship
