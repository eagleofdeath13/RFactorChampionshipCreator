"""
Service for importing talents from CSV files.

Supports importing driver lists from CSV format into rFactor talent files.
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

from ..models.talent import Talent, TalentPersonalInfo, TalentStats
from .talent_service import TalentService
from ..utils.talent_randomizer import TalentRandomizer


@dataclass
class ImportResult:
    """Result of a CSV import operation."""

    success_count: int = 0
    error_count: int = 0
    overwrite_count: int = 0
    errors: List[Tuple[int, str, str]] = field(default_factory=list)  # (row_number, talent_name, error_message)
    warnings: List[Tuple[int, str, str]] = field(default_factory=list)  # (row_number, talent_name, warning_message)

    @property
    def total(self) -> int:
        """Total number of rows processed."""
        return self.success_count + self.error_count

    def add_success(self, overwrite: bool = False):
        """Mark a successful import."""
        self.success_count += 1
        if overwrite:
            self.overwrite_count += 1

    def add_error(self, row_num: int, name: str, error: str):
        """Add an error to the result."""
        self.error_count += 1
        self.errors.append((row_num, name, error))

    def add_warning(self, row_num: int, name: str, warning: str):
        """Add a warning to the result."""
        self.warnings.append((row_num, name, warning))


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
    def parse_csv_row(row: Dict[str, str], row_num: int, fill_missing: bool = True) -> Talent:
        """
        Parse a CSV row into a Talent object.

        Args:
            row: Dictionary of column_name -> value
            row_num: Row number (for error reporting)
            fill_missing: If True, use TalentRandomizer to fill missing/empty fields

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

        # Prepare data dict for randomizer
        data = {'name': name}

        # Helper to get value or None/empty
        def get_value(key, convert_fn=str, default=''):
            val = row.get(key, default).strip()
            if not val or val == '':
                return None
            try:
                return convert_fn(val)
            except (ValueError, TypeError):
                return None

        # Extract all fields (None if missing/empty)
        data['nationality'] = get_value('nationality')
        data['date_of_birth'] = get_value('date_of_birth')
        data['starts'] = get_value('starts', int, 0)
        data['poles'] = get_value('poles', int, 0)
        data['wins'] = get_value('wins', int, 0)
        data['drivers_championships'] = get_value('drivers_championships', int, 0)
        data['aggression'] = get_value('aggression', float)
        data['reputation'] = get_value('reputation', float)
        data['courtesy'] = get_value('courtesy', float)
        data['composure'] = get_value('composure', float)
        data['speed'] = get_value('speed', float)
        data['crash'] = get_value('crash', float)
        data['recovery'] = get_value('recovery', float)
        data['completed_laps'] = get_value('completed_laps', float)
        data['min_racing_skill'] = get_value('min_racing_skill', float)

        # Fill missing fields with randomizer if requested
        if fill_missing:
            data = TalentRandomizer.fill_missing_fields(data)

        # Create talent objects
        try:
            personal_info = TalentPersonalInfo(
                nationality=data['nationality'],
                date_of_birth=data['date_of_birth'],
                starts=int(data['starts']) if data['starts'] is not None else 0,
                poles=int(data['poles']) if data['poles'] is not None else 0,
                wins=int(data['wins']) if data['wins'] is not None else 0,
                drivers_championships=int(data['drivers_championships']) if data['drivers_championships'] is not None else 0,
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Row {row_num}: Invalid personal info - {e}")

        try:
            stats = TalentStats(
                aggression=float(data['aggression']),
                reputation=float(data['reputation']),
                courtesy=float(data['courtesy']),
                composure=float(data['composure']),
                speed=float(data['speed']),
                crash=float(data['crash']),
                recovery=float(data['recovery']),
                completed_laps=float(data['completed_laps']),
                min_racing_skill=float(data['min_racing_skill']),
            )
        except (ValueError, TypeError) as e:
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
        overwrite_existing: bool = True,
        fill_missing: bool = True,
        validate_only: bool = False,
    ) -> ImportResult:
        """
        Import talents from a CSV file.

        Args:
            csv_path: Path to the CSV file
            overwrite_existing: If True, overwrite talents that already exist (default: True)
            fill_missing: If True, use randomizer to fill missing/empty fields (default: True)
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
                    # Parse talent from row (with optional field filling)
                    talent = self.parse_csv_row(row, row_num, fill_missing=fill_missing)

                    # Check if talent already exists
                    talent_exists = self.talent_service.exists(talent.name)

                    if talent_exists:
                        if overwrite_existing:
                            # Overwrite existing talent
                            if not validate_only:
                                self.talent_service.update(talent.name, talent)
                            result.add_success(overwrite=True)
                            result.add_warning(
                                row_num,
                                talent.name,
                                "Talent already exists - overwritten with CSV data"
                            )
                        else:
                            # Skip existing talent
                            result.add_error(
                                row_num,
                                talent.name,
                                "Talent already exists (skipped - overwrite disabled)"
                            )
                            continue
                    else:
                        # Create new talent
                        if not validate_only:
                            self.talent_service.create(talent)
                        result.add_success(overwrite=False)

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
