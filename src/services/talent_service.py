"""
Service for managing rFactor Talents (drivers).

Provides methods to list, get, create, and search talents.
"""

from pathlib import Path
from typing import List, Optional

from ..models.talent import Talent
from ..parsers.rcd_parser import RCDParser
from ..generators.rcd_generator import RCDGenerator
from ..utils.file_utils import find_files_by_extension, normalize_name_to_filename
from ..utils.rfactor_validator import RFactorValidator


class TalentService:
    """Service for managing talents."""

    def __init__(self, rfactor_path: str, validate: bool = True):
        """
        Initialize the TalentService.

        Args:
            rfactor_path: Path to the rFactor installation directory
            validate: Whether to validate the rFactor installation (default: True)

        Raises:
            ValueError: If validate=True and the path is invalid
        """
        self.rfactor_path = Path(rfactor_path)

        # Validate rFactor installation if requested
        if validate:
            RFactorValidator.validate_or_raise(str(self.rfactor_path))

        self.talent_dir = self.rfactor_path / "GameData" / "Talent"

        if not self.talent_dir.exists():
            raise ValueError(f"Talent directory not found: {self.talent_dir}")

    def list_all(self) -> List[str]:
        """
        List all available talents (names only).

        Returns:
            List of talent names
        """
        rcd_files = find_files_by_extension(str(self.talent_dir), '.rcd', recursive=False)

        # Filter out Dialog.ini if present
        rcd_files = [f for f in rcd_files if f.stem != 'Dialog']

        return sorted([f.stem for f in rcd_files])

    def list_all_talents(self) -> List[Talent]:
        """
        List all available talents (full Talent objects).

        Returns:
            List of Talent objects

        Note: This can be slow for large talent directories.
        """
        names = self.list_all()
        talents = []

        for name in names:
            try:
                talent = self.get_by_filename(name)
                if talent is not None:
                    talents.append(talent)
            except Exception:
                # Skip talents that can't be parsed
                continue

        return talents

    def get(self, name: str) -> Optional[Talent]:
        """
        Get a talent by name.

        Args:
            name: Name of the talent (e.g., "Brandon Lang")

        Returns:
            Talent object or None if not found
        """
        filename = normalize_name_to_filename(name)
        return self.get_by_filename(filename)

    def get_by_filename(self, filename: str) -> Optional[Talent]:
        """
        Get a talent by filename (without extension).

        Args:
            filename: Filename without extension (e.g., "BrandonLang")

        Returns:
            Talent object or None if not found
        """
        # Ensure .rcd extension
        if not filename.endswith('.rcd'):
            filename = f"{filename}.rcd"

        filepath = self.talent_dir / filename

        if not filepath.exists():
            return None

        try:
            return RCDParser.parse_file(str(filepath))
        except Exception:
            return None

    def exists(self, name: str) -> bool:
        """
        Check if a talent exists.

        Args:
            name: Name of the talent

        Returns:
            True if talent exists, False otherwise
        """
        return self.get(name) is not None

    def create(self, talent: Talent) -> None:
        """
        Create a new talent.

        Args:
            talent: Talent object to create

        Raises:
            FileExistsError: If talent already exists
        """
        filename = normalize_name_to_filename(talent.name) + '.rcd'
        filepath = self.talent_dir / filename

        if filepath.exists():
            raise FileExistsError(f"Talent already exists: {talent.name}")

        RCDGenerator.generate(talent, str(filepath))

    def update(self, talent: Talent) -> None:
        """
        Update an existing talent.

        Args:
            talent: Talent object to update

        Raises:
            FileNotFoundError: If talent doesn't exist
        """
        filename = normalize_name_to_filename(talent.name) + '.rcd'
        filepath = self.talent_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Talent not found: {talent.name}")

        RCDGenerator.generate(talent, str(filepath))

    def delete(self, name: str) -> None:
        """
        Delete a talent.

        Args:
            name: Name of the talent to delete

        Raises:
            FileNotFoundError: If talent doesn't exist
        """
        filename = normalize_name_to_filename(name) + '.rcd'
        filepath = self.talent_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Talent not found: {name}")

        filepath.unlink()

    def search(self, query: str) -> List[Talent]:
        """
        Search talents by name.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching Talent objects
        """
        query_lower = query.lower()
        names = self.list_all()

        matching_talents = []
        for name in names:
            if query_lower in name.lower():
                talent = self.get_by_filename(name)
                if talent:
                    matching_talents.append(talent)

        return matching_talents

    def get_by_nationality(self, nationality: str) -> List[Talent]:
        """
        Get all talents of a specific nationality.

        Args:
            nationality: Nationality to filter by

        Returns:
            List of Talent objects
        """
        all_talents = self.list_all_talents()
        return [
            t for t in all_talents
            if t.personal_info.nationality.lower() == nationality.lower()
        ]

    def get_stats_summary(self, name: str) -> Optional[dict]:
        """
        Get a summary of a talent's stats.

        Args:
            name: Name of the talent

        Returns:
            Dictionary with stats summary or None if not found
        """
        talent = self.get(name)
        if not talent:
            return None

        return {
            'name': talent.name,
            'nationality': talent.personal_info.nationality,
            'speed': talent.stats.speed,
            'aggression': talent.stats.aggression,
            'composure': talent.stats.composure,
            'wins': talent.personal_info.wins,
            'poles': talent.personal_info.poles,
            'championships': talent.personal_info.drivers_championships,
        }
