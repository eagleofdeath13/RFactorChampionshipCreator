"""Tests for Import Service."""

import pytest
import tempfile
import csv
from pathlib import Path

from src.services.import_service import ImportService, ImportResult
from src.services.talent_service import TalentService
from src.models.talent import Talent, TalentPersonalInfo, TalentStats


class TestImportService:
    """Test suite for ImportService."""

    @pytest.fixture
    def temp_rfactor_dir(self):
        """Create a temporary rFactor directory structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create required directories
            (temp_path / "rFactor.exe").touch()
            (temp_path / "GameData").mkdir()
            (temp_path / "UserData").mkdir()

            talent_dir = temp_path / "GameData" / "Talent"
            talent_dir.mkdir(parents=True)

            yield temp_path

    @pytest.fixture
    def talent_service(self, temp_rfactor_dir):
        """Create a TalentService with temp directory."""
        return TalentService(str(temp_rfactor_dir), validate=False)

    @pytest.fixture
    def import_service(self, talent_service):
        """Create an ImportService."""
        return ImportService(talent_service)

    def test_validate_csv_headers_valid(self, import_service):
        """Test validation of valid CSV headers."""
        headers = ['name', 'nationality', 'date_of_birth', 'speed']
        is_valid, error = ImportService.validate_csv_headers(headers)

        assert is_valid is True
        assert error is None

    def test_validate_csv_headers_missing_required(self, import_service):
        """Test validation fails when required headers are missing."""
        headers = ['name', 'nationality']  # Missing date_of_birth
        is_valid, error = ImportService.validate_csv_headers(headers)

        assert is_valid is False
        assert 'date_of_birth' in error

    def test_validate_csv_headers_case_insensitive(self, import_service):
        """Test header validation is case insensitive."""
        headers = ['NAME', 'NATIONALITY', 'Date_Of_Birth']
        is_valid, error = ImportService.validate_csv_headers(headers)

        assert is_valid is True

    def test_parse_csv_row_minimal(self, import_service):
        """Test parsing a CSV row with minimal data."""
        row = {
            'name': 'Test Driver',
            'nationality': 'France',
            'date_of_birth': '15-03-1990',
        }

        talent = ImportService.parse_csv_row(row, 1)

        assert talent.name == 'Test Driver'
        assert talent.personal_info.nationality == 'France'
        assert talent.personal_info.date_of_birth == '15-03-1990'
        assert talent.personal_info.starts == 0
        assert talent.stats.speed == 50.0  # Default value

    def test_parse_csv_row_full(self, import_service):
        """Test parsing a CSV row with all fields."""
        row = {
            'name': 'Full Driver',
            'nationality': 'Germany',
            'date_of_birth': '20-05-1985',
            'starts': '100',
            'poles': '10',
            'wins': '5',
            'drivers_championships': '2',
            'aggression': '75.5',
            'reputation': '80.0',
            'courtesy': '70.0',
            'composure': '85.0',
            'speed': '90.0',
            'crash': '30.0',
            'recovery': '75.0',
            'completed_laps': '95.0',
            'min_racing_skill': '80.0',
        }

        talent = ImportService.parse_csv_row(row, 1)

        assert talent.name == 'Full Driver'
        assert talent.personal_info.nationality == 'Germany'
        assert talent.personal_info.starts == 100
        assert talent.personal_info.poles == 10
        assert talent.personal_info.wins == 5
        assert talent.personal_info.drivers_championships == 2
        assert talent.stats.aggression == 75.5
        assert talent.stats.speed == 90.0

    def test_parse_csv_row_missing_name(self, import_service):
        """Test parsing fails when name is missing."""
        row = {
            'name': '',
            'nationality': 'France',
            'date_of_birth': '01-01-1990',
        }

        with pytest.raises(ValueError, match="Name is required"):
            ImportService.parse_csv_row(row, 1)

    def test_parse_csv_row_invalid_stat_range(self, import_service):
        """Test parsing fails when stat is out of range."""
        row = {
            'name': 'Test Driver',
            'nationality': 'France',
            'date_of_birth': '01-01-1990',
            'speed': '150.0',  # Invalid: > 100
        }

        with pytest.raises(ValueError, match="Invalid stats"):
            ImportService.parse_csv_row(row, 1)

    def test_parse_csv_row_invalid_personal_info(self, import_service):
        """Test parsing fails with invalid personal info."""
        row = {
            'name': 'Test Driver',
            'nationality': 'France',
            'date_of_birth': '01-01-1990',
            'starts': '-5',  # Invalid: negative
        }

        with pytest.raises(ValueError, match="Invalid personal info"):
            ImportService.parse_csv_row(row, 1)

    def test_generate_csv_template(self, import_service):
        """Test generating a CSV template file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name

        try:
            ImportService.generate_csv_template(temp_file)

            # Verify file exists and has content
            assert Path(temp_file).exists()

            # Read and verify structure
            with open(temp_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                # Should have 2 example rows
                assert len(rows) == 2

                # Check headers
                assert 'name' in reader.fieldnames
                assert 'nationality' in reader.fieldnames
                assert 'speed' in reader.fieldnames

                # Check first row
                assert rows[0]['name'] == 'Example Driver 1'
                assert rows[0]['nationality'] == 'France'

        finally:
            Path(temp_file).unlink()

    def test_import_from_csv_success(self, import_service, talent_service):
        """Test successful import from CSV."""
        # Create test CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as f:
            temp_file = f.name
            writer = csv.DictWriter(f, fieldnames=['name', 'nationality', 'date_of_birth', 'speed'])
            writer.writeheader()
            writer.writerow({
                'name': 'Import Test 1',
                'nationality': 'Italy',
                'date_of_birth': '10-10-1988',
                'speed': '85.0',
            })
            writer.writerow({
                'name': 'Import Test 2',
                'nationality': 'Spain',
                'date_of_birth': '20-12-1992',
                'speed': '78.0',
            })

        try:
            result = import_service.import_from_csv(temp_file, skip_existing=False)

            assert result.success_count == 2
            assert result.error_count == 0
            assert result.total == 2

            # Verify talents were created
            talent1 = talent_service.get('Import Test 1')
            assert talent1 is not None
            assert talent1.personal_info.nationality == 'Italy'
            assert talent1.stats.speed == 85.0

            talent2 = talent_service.get('Import Test 2')
            assert talent2 is not None

        finally:
            Path(temp_file).unlink()

    def test_import_from_csv_skip_existing(self, import_service, talent_service):
        """Test import skips existing talents."""
        # Create a talent first
        existing = Talent(
            name='Existing Driver',
            personal_info=TalentPersonalInfo(
                nationality='France',
                date_of_birth='01-01-1990',
            ),
            stats=TalentStats(),
        )
        talent_service.create(existing)

        # Create CSV with existing talent
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as f:
            temp_file = f.name
            writer = csv.DictWriter(f, fieldnames=['name', 'nationality', 'date_of_birth'])
            writer.writeheader()
            writer.writerow({
                'name': 'Existing Driver',
                'nationality': 'Germany',
                'date_of_birth': '02-02-1992',
            })

        try:
            result = import_service.import_from_csv(temp_file, skip_existing=True)

            assert result.success_count == 0
            assert result.error_count == 1
            assert 'already exists' in result.errors[0][2].lower()

            # Verify original talent wasn't modified
            talent = talent_service.get('Existing Driver')
            assert talent.personal_info.nationality == 'France'  # Original value

        finally:
            Path(temp_file).unlink()

    def test_import_from_csv_validate_only(self, import_service, talent_service):
        """Test validate-only mode doesn't create talents."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as f:
            temp_file = f.name
            writer = csv.DictWriter(f, fieldnames=['name', 'nationality', 'date_of_birth'])
            writer.writeheader()
            writer.writerow({
                'name': 'Validation Test',
                'nationality': 'France',
                'date_of_birth': '01-01-1990',
            })

        try:
            result = import_service.import_from_csv(temp_file, validate_only=True)

            assert result.success_count == 1
            assert result.error_count == 0

            # Verify talent was NOT created
            talent = talent_service.get('Validation Test')
            assert talent is None

        finally:
            Path(temp_file).unlink()

    def test_import_from_csv_partial_errors(self, import_service):
        """Test import continues after errors."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as f:
            temp_file = f.name
            writer = csv.DictWriter(f, fieldnames=['name', 'nationality', 'date_of_birth', 'speed'])
            writer.writeheader()
            writer.writerow({
                'name': 'Good Driver',
                'nationality': 'France',
                'date_of_birth': '01-01-1990',
                'speed': '80.0',
            })
            writer.writerow({
                'name': 'Bad Driver',
                'nationality': 'Germany',
                'date_of_birth': '02-02-1992',
                'speed': '999.0',  # Invalid
            })
            writer.writerow({
                'name': 'Another Good',
                'nationality': 'Italy',
                'date_of_birth': '03-03-1994',
                'speed': '75.0',
            })

        try:
            result = import_service.import_from_csv(temp_file)

            assert result.success_count == 2
            assert result.error_count == 1
            assert result.total == 3
            assert len(result.errors) == 1
            assert result.errors[0][1] == 'Bad Driver'

        finally:
            Path(temp_file).unlink()

    def test_import_from_csv_file_not_found(self, import_service):
        """Test import raises error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            import_service.import_from_csv('nonexistent.csv')

    def test_import_from_csv_invalid_headers(self, import_service):
        """Test import raises error for invalid headers."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as f:
            temp_file = f.name
            writer = csv.DictWriter(f, fieldnames=['name', 'nationality'])  # Missing date_of_birth
            writer.writeheader()

        try:
            with pytest.raises(ValueError, match="Missing required columns"):
                import_service.import_from_csv(temp_file)
        finally:
            Path(temp_file).unlink()

    def test_export_to_csv(self, import_service, talent_service):
        """Test exporting talents to CSV."""
        # Create some talents
        talent1 = Talent(
            name='Export Test 1',
            personal_info=TalentPersonalInfo(
                nationality='France',
                date_of_birth='15-03-1990',
                starts=50,
                wins=5,
            ),
            stats=TalentStats(speed=85.0, aggression=70.0),
        )
        talent2 = Talent(
            name='Export Test 2',
            personal_info=TalentPersonalInfo(
                nationality='Germany',
                date_of_birth='20-07-1988',
            ),
            stats=TalentStats(speed=78.0),
        )

        talent_service.create(talent1)
        talent_service.create(talent2)

        # Export to CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name

        try:
            count = import_service.export_to_csv(temp_file)

            assert count == 2

            # Verify CSV content
            with open(temp_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                assert len(rows) == 2
                assert rows[0]['name'] == 'Export Test 1'
                assert rows[0]['nationality'] == 'France'
                assert rows[0]['speed'] == '85.0'
                assert rows[1]['name'] == 'Export Test 2'

        finally:
            Path(temp_file).unlink()

    def test_export_to_csv_specific_talents(self, import_service, talent_service):
        """Test exporting specific talents to CSV."""
        # Create talents
        for i in range(5):
            talent = Talent(
                name=f'Driver {i}',
                personal_info=TalentPersonalInfo(
                    nationality='France',
                    date_of_birth='01-01-1990',
                ),
                stats=TalentStats(),
            )
            talent_service.create(talent)

        # Export only 2 specific talents
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name

        try:
            count = import_service.export_to_csv(
                temp_file,
                talent_names=['Driver 1', 'Driver 3']
            )

            assert count == 2

            # Verify only specified talents exported
            with open(temp_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                assert len(rows) == 2
                names = [row['name'] for row in rows]
                assert 'Driver 1' in names
                assert 'Driver 3' in names
                assert 'Driver 0' not in names

        finally:
            Path(temp_file).unlink()

    def test_export_nonexistent_talent_raises_error(self, import_service):
        """Test export raises error for non-existent talent."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="Talent not found"):
                import_service.export_to_csv(temp_file, talent_names=['Nonexistent'])
        finally:
            Path(temp_file).unlink()

    def test_import_result_properties(self):
        """Test ImportResult helper properties."""
        result = ImportResult()
        assert result.total == 0

        result.add_success()
        result.add_success()
        assert result.success_count == 2
        assert result.total == 2

        result.add_error(3, 'Test', 'Error message')
        assert result.error_count == 1
        assert result.total == 3
        assert len(result.errors) == 1
        assert result.errors[0] == (3, 'Test', 'Error message')
