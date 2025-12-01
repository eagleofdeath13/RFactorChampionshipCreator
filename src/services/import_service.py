"""
Service for importing talents from CSV files.

Supports importing driver lists from CSV format into rFactor talent files.
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from ..models.talent import Talent, TalentPersonalInfo, TalentStats
from .talent_service import TalentService


@dataclass
class ImportResult:
    """Result of a CSV import operation."""

    success_count: int = 0
    error_count: int = 0
    errors: List[Tuple[int, str, str]] = None  # (row_number, talent_name, error_message)

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

    @property
    def total(self) -> int:
        """Total number of rows processed."""
        return self.success_count + self.error_count

    def add_success(self):
        """Mark a successful import."""
        self.success_count += 1

    def add_error(self, row_num: int, name: str, error: str):
        """Add an error to the result."""
        self.error_count += 1
        self.errors.append((row_num, name, error))


class ImportService:
    """Service for importing talents from CSV files."""

    # Expected CSV columns
    REQUIRED_COLUMNS = ['name', 'nationality', 'date_of_birth']

    PERSONAL_INFO_COLUMNS = [
        'nationality', 'date_of_birth', 'starts', 'poles', 'wins',
        'drivers_championships'
    ]

    STATS_COLUMNS = [
        'aggression', 'reputation', 'courtesy', 'composure', 'speed',
        'crash', 'recovery', 'completed_laps', 'min_racing_skill'
    ]

    ALL_COLUMNS = ['name'] + PERSONAL_INFO_COLUMNS + STATS_COLUMNS

    def __init__(self, talent_service: TalentService):
        """
        Initialize the ImportService.

        Args:
            talent_service: TalentService instance for creating talents
        """
        self.talent_service = talent_service

    @staticmethod
    def validate_csv_headers(headers: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Validate that CSV has required headers.

        Args:
            headers: List of column headers from CSV

        Returns:
            Tuple of (is_valid, error_message)
        """
        headers_lower = [h.lower().strip() for h in headers]

        # Check for required columns
        missing = []
        for col in ImportService.REQUIRED_COLUMNS:
            if col not in headers_lower:
                missing.append(col)

        if missing:
            return False, f"Missing required columns: {', '.join(missing)}"

        return True, None

    @staticmethod
    def parse_csv_row(row: Dict[str, str], row_num: int) -> Talent:
        """
        Parse a CSV row into a Talent object.

        Args:
            row: Dictionary of column_name -> value
            row_num: Row number (for error reporting)

        Returns:
            Talent object

        Raises:
            ValueError: If row data is invalid
        """
        # Normalize keys to lowercase
        row = {k.lower().strip(): v.strip() for k, v in row.items()}

        # Extract name
        name = row.get('name', '').strip()
        if not name:
            raise ValueError(f"Row {row_num}: Name is required")

        # Parse personal info
        try:
            personal_info = TalentPersonalInfo(
                nationality=row.get('nationality', 'Unknown'),
                date_of_birth=row.get('date_of_birth', '01-01-1980'),
                starts=int(row.get('starts', 0)),
                poles=int(row.get('poles', 0)),
                wins=int(row.get('wins', 0)),
                drivers_championships=int(row.get('drivers_championships', 0)),
            )
        except ValueError as e:
            raise ValueError(f"Row {row_num}: Invalid personal info - {e}")

        # Parse stats (with defaults)
        try:
            stats = TalentStats(
                aggression=float(row.get('aggression', 50.0)),
                reputation=float(row.get('reputation', 50.0)),
                courtesy=float(row.get('courtesy', 50.0)),
                composure=float(row.get('composure', 50.0)),
                speed=float(row.get('speed', 50.0)),
                crash=float(row.get('crash', 50.0)),
                recovery=float(row.get('recovery', 50.0)),
                completed_laps=float(row.get('completed_laps', 90.0)),
                min_racing_skill=float(row.get('min_racing_skill', 50.0)),
            )
        except ValueError as e:
            raise ValueError(f"Row {row_num}: Invalid stats - {e}")

        # Create talent
        return Talent(
            name=name,
            personal_info=personal_info,
            stats=stats,
        )

    def import_from_csv(
        self,
        csv_path: str,
        skip_existing: bool = True,
        validate_only: bool = False,
    ) -> ImportResult:
        """
        Import talents from a CSV file.

        Args:
            csv_path: Path to the CSV file
            skip_existing: If True, skip talents that already exist
            validate_only: If True, only validate without creating files

        Returns:
            ImportResult with success/error counts and details

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV format is invalid
        """
        csv_file = Path(csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        result = ImportResult()

        # Read CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Validate headers
            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no headers")

            is_valid, error = self.validate_csv_headers(reader.fieldnames)
            if not is_valid:
                raise ValueError(error)

            # Process each row
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                try:
                    # Parse talent from row
                    talent = self.parse_csv_row(row, row_num)

                    # Check if talent already exists
                    if skip_existing and self.talent_service.exists(talent.name):
                        result.add_error(
                            row_num,
                            talent.name,
                            "Talent already exists (skipped)"
                        )
                        continue

                    # Create talent (if not validate-only mode)
                    if not validate_only:
                        self.talent_service.create(talent)

                    result.add_success()

                except ValueError as e:
                    result.add_error(row_num, row.get('name', 'Unknown'), str(e))
                except Exception as e:
                    result.add_error(
                        row_num,
                        row.get('name', 'Unknown'),
                        f"Unexpected error: {e}"
                    )

        return result

    @staticmethod
    def generate_csv_template(output_path: str) -> None:
        """
        Generate a CSV template file with example data.

        Args:
            output_path: Path where to save the template CSV
        """
        template_data = [
            {
                'name': 'Example Driver 1',
                'nationality': 'France',
                'date_of_birth': '15-03-1985',
                'starts': 100,
                'poles': 10,
                'wins': 5,
                'drivers_championships': 1,
                'aggression': 75.0,
                'reputation': 80.0,
                'courtesy': 70.0,
                'composure': 85.0,
                'speed': 90.0,
                'crash': 30.0,
                'recovery': 75.0,
                'completed_laps': 95.0,
                'min_racing_skill': 80.0,
            },
            {
                'name': 'Example Driver 2',
                'nationality': 'Germany',
                'date_of_birth': '22-07-1990',
                'starts': 50,
                'poles': 3,
                'wins': 1,
                'drivers_championships': 0,
                'aggression': 60.0,
                'reputation': 65.0,
                'courtesy': 80.0,
                'composure': 70.0,
                'speed': 75.0,
                'crash': 40.0,
                'recovery': 65.0,
                'completed_laps': 92.0,
                'min_racing_skill': 65.0,
            },
        ]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=ImportService.ALL_COLUMNS)
            writer.writeheader()
            writer.writerows(template_data)

    def export_to_csv(self, output_path: str, talent_names: Optional[List[str]] = None) -> int:
        """
        Export talents to CSV file.

        Args:
            output_path: Path where to save the CSV
            talent_names: Optional list of talent names to export (None = all)

        Returns:
            Number of talents exported

        Raises:
            ValueError: If a talent doesn't exist
        """
        # Get talents to export
        if talent_names is None:
            talents = self.talent_service.list_all_talents()
        else:
            talents = []
            for name in talent_names:
                talent = self.talent_service.get(name)
                if not talent:
                    raise ValueError(f"Talent not found: {name}")
                talents.append(talent)

        # Write to CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.ALL_COLUMNS)
            writer.writeheader()

            for talent in talents:
                row = {
                    'name': talent.name,
                    'nationality': talent.personal_info.nationality,
                    'date_of_birth': talent.personal_info.date_of_birth,
                    'starts': talent.personal_info.starts,
                    'poles': talent.personal_info.poles,
                    'wins': talent.personal_info.wins,
                    'drivers_championships': talent.personal_info.drivers_championships,
                    'aggression': talent.stats.aggression,
                    'reputation': talent.stats.reputation,
                    'courtesy': talent.stats.courtesy,
                    'composure': talent.stats.composure,
                    'speed': talent.stats.speed,
                    'crash': talent.stats.crash,
                    'recovery': talent.stats.recovery,
                    'completed_laps': talent.stats.completed_laps,
                    'min_racing_skill': talent.stats.min_racing_skill,
                }
                writer.writerow(row)

        return len(talents)
