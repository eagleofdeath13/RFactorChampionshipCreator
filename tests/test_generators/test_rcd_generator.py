"""Tests for RCD Generator."""

import pytest
from pathlib import Path
import tempfile
import os

from src.generators.rcd_generator import RCDGenerator
from src.parsers.rcd_parser import RCDParser
from src.models.talent import Talent, TalentPersonalInfo, TalentStats


class TestRCDGenerator:
    """Test suite for RCDGenerator."""

    def test_to_content_basic(self):
        """Test generating content from a Talent object."""
        personal_info = TalentPersonalInfo(
            nationality="French",
            date_of_birth="15-05-1990",
            starts=20,
            poles=5,
            wins=3,
            drivers_championships=1,
        )

        stats = TalentStats(
            aggression=80.0,
            reputation=75.5,
            courtesy=70.0,
            composure=85.0,
            speed=90.0,
            crash=10.0,
            recovery=80.0,
            completed_laps=95.0,
            min_racing_skill=85.0,
        )

        talent = Talent(
            name="John Doe",
            personal_info=personal_info,
            stats=stats,
        )

        content = RCDGenerator.to_content(talent)

        # Check that content contains expected elements
        assert "John Doe" in content
        assert "Nationality=French" in content
        assert "DateofBirth=15-05-1990" in content
        assert "Starts=20" in content
        assert "Speed=90.00" in content
        assert "//Driver Info" in content
        assert "//Driver Stats" in content
        assert content.startswith("John Doe")
        assert "{" in content
        assert "}" in content

    def test_generate_and_read_back(self):
        """Test round-trip: generate file and parse it back."""
        # Create a talent
        personal_info = TalentPersonalInfo(
            nationality="German",
            date_of_birth="03-07-1987",
            starts=50,
            poles=15,
            wins=12,
            drivers_championships=2,
        )

        stats = TalentStats(
            aggression=85.5,
            reputation=92.0,
            courtesy=75.0,
            composure=88.0,
            speed=95.5,
            crash=8.0,
            recovery=85.0,
            completed_laps=97.0,
            min_racing_skill=90.0,
        )

        original_talent = Talent(
            name="Sebastian Vettel",
            personal_info=personal_info,
            stats=stats,
        )

        # Generate file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.rcd', delete=False, encoding='cp1252') as f:
            temp_file = f.name

        try:
            RCDGenerator.generate(original_talent, temp_file)

            # Parse it back
            parsed_talent = RCDParser.parse_file(temp_file)

            # Compare
            assert parsed_talent.name == original_talent.name
            assert parsed_talent.personal_info.nationality == original_talent.personal_info.nationality
            assert parsed_talent.personal_info.starts == original_talent.personal_info.starts
            assert parsed_talent.stats.speed == pytest.approx(original_talent.stats.speed)
            assert parsed_talent.stats.aggression == pytest.approx(original_talent.stats.aggression)

        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_generate_with_name_spaces(self):
        """Test generating talent with spaces in name."""
        personal_info = TalentPersonalInfo(
            nationality="Spanish",
            date_of_birth="29-07-1981",
            starts=100,
            poles=20,
            wins=30,
            drivers_championships=2,
        )

        stats = TalentStats(speed=98.0)

        talent = Talent(
            name="Fernando Alonso",
            personal_info=personal_info,
            stats=stats,
        )

        content = RCDGenerator.to_content(talent)

        # Name should be preserved with spaces
        assert content.startswith("Fernando Alonso\n")

    def test_generate_stats_formatting(self):
        """Test that stats are formatted with 2 decimal places."""
        personal_info = TalentPersonalInfo(
            nationality="British",
            date_of_birth="07-01-1985",
        )

        stats = TalentStats(
            speed=95.123456,  # Should be rounded to 95.12
            aggression=80.9,  # Should be 80.90
        )

        talent = Talent(
            name="Lewis Hamilton",
            personal_info=personal_info,
            stats=stats,
        )

        content = RCDGenerator.to_content(talent)

        assert "Speed=95.12" in content
        assert "Aggression=80.90" in content

    def test_generate_creates_directories(self):
        """Test that generator creates parent directories if needed."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create path with non-existent subdirectories
            filepath = Path(temp_dir) / "subdir1" / "subdir2" / "test.rcd"

            personal_info = TalentPersonalInfo(
                nationality="Italian",
                date_of_birth="01-01-1990",
            )
            stats = TalentStats()
            talent = Talent(
                name="Test Driver",
                personal_info=personal_info,
                stats=stats,
            )

            # Should not raise an error
            RCDGenerator.generate(talent, str(filepath))

            # Check file was created
            assert filepath.exists()

    def test_round_trip_preserves_data(self):
        """Test that generating and parsing preserves all data accurately."""
        # Use real example file
        fixtures_dir = Path(__file__).parent.parent / "fixtures"
        brandon_lang_file = fixtures_dir / "BrandonLang.rcd"

        if brandon_lang_file.exists():
            # Parse original
            original = RCDParser.parse_file(str(brandon_lang_file))

            # Generate to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rcd', delete=False, encoding='cp1252') as f:
                temp_file = f.name

            try:
                RCDGenerator.generate(original, temp_file)

                # Parse generated file
                regenerated = RCDParser.parse_file(temp_file)

                # Compare all fields
                assert regenerated.name == original.name

                # Personal info
                assert regenerated.personal_info.nationality == original.personal_info.nationality
                assert regenerated.personal_info.date_of_birth == original.personal_info.date_of_birth
                assert regenerated.personal_info.starts == original.personal_info.starts
                assert regenerated.personal_info.poles == original.personal_info.poles
                assert regenerated.personal_info.wins == original.personal_info.wins
                assert regenerated.personal_info.drivers_championships == original.personal_info.drivers_championships

                # Stats (with tolerance for floating point)
                assert regenerated.stats.aggression == pytest.approx(original.stats.aggression, abs=0.01)
                assert regenerated.stats.reputation == pytest.approx(original.stats.reputation, abs=0.01)
                assert regenerated.stats.courtesy == pytest.approx(original.stats.courtesy, abs=0.01)
                assert regenerated.stats.composure == pytest.approx(original.stats.composure, abs=0.01)
                assert regenerated.stats.speed == pytest.approx(original.stats.speed, abs=0.01)
                assert regenerated.stats.crash == pytest.approx(original.stats.crash, abs=0.01)
                assert regenerated.stats.recovery == pytest.approx(original.stats.recovery, abs=0.01)
                assert regenerated.stats.completed_laps == pytest.approx(original.stats.completed_laps, abs=0.01)
                assert regenerated.stats.min_racing_skill == pytest.approx(original.stats.min_racing_skill, abs=0.01)

            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
