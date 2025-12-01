"""Tests for RCD Parser."""

import pytest
from pathlib import Path

from src.parsers.rcd_parser import RCDParser, RCDParseError
from src.models.talent import Talent, TalentPersonalInfo, TalentStats


# Test fixtures path
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
BRANDON_LANG_FILE = FIXTURES_DIR / "BrandonLang.rcd"


class TestRCDParser:
    """Test suite for RCDParser."""

    def test_parse_file_brandon_lang(self):
        """Test parsing the Brandon Lang example file."""
        talent = RCDParser.parse_file(str(BRANDON_LANG_FILE))

        assert talent.name == "Brandon Lang"
        assert talent.personal_info.nationality == "American"
        assert talent.personal_info.date_of_birth == "28-11-1984"
        assert talent.personal_info.starts == 9
        assert talent.personal_info.poles == 2
        assert talent.personal_info.wins == 0
        assert talent.personal_info.drivers_championships == 0

        assert talent.stats.aggression == pytest.approx(74.73)
        assert talent.stats.reputation == pytest.approx(57.89)
        assert talent.stats.courtesy == pytest.approx(61.88)
        assert talent.stats.composure == pytest.approx(88.35)
        assert talent.stats.speed == pytest.approx(95.13)
        assert talent.stats.crash == pytest.approx(4.87)
        assert talent.stats.recovery == pytest.approx(83.62)
        assert talent.stats.completed_laps == pytest.approx(91.71)
        assert talent.stats.min_racing_skill == pytest.approx(89.00)

    def test_parse_content_basic(self):
        """Test parsing basic content."""
        content = """John Doe
{
//Driver Info
  Nationality=French
  DateofBirth=15-05-1990
  Starts=20
  Poles=5
  Wins=3
  DriversChampionships=1

//Driver Stats
  Aggression=80.00
  Reputation=75.50
  Courtesy=70.00
  Composure=85.00
  Speed=90.00
  Crash=10.00
  Recovery=80.00
  CompletedLaps=95.00
  MinRacingSkill=85.00
}
"""
        talent = RCDParser.parse_content(content)

        assert talent.name == "John Doe"
        assert talent.personal_info.nationality == "French"
        assert talent.stats.speed == pytest.approx(90.0)

    def test_parse_content_with_spaces_in_name(self):
        """Test parsing talent with spaces in name."""
        content = """Fernando Alonso Diaz
{
//Driver Info
  Nationality=Spanish
  DateofBirth=29-07-1981
  Starts=100
  Poles=20
  Wins=30
  DriversChampionships=2

//Driver Stats
  Aggression=85.00
  Reputation=95.00
  Courtesy=80.00
  Composure=90.00
  Speed=98.00
  Crash=5.00
  Recovery=90.00
  CompletedLaps=98.00
  MinRacingSkill=95.00
}
"""
        talent = RCDParser.parse_content(content)

        assert talent.name == "Fernando Alonso Diaz"
        assert talent.personal_info.drivers_championships == 2

    def test_parse_content_missing_braces(self):
        """Test that parsing fails when braces are missing."""
        content = """John Doe
Nationality=French
"""
        with pytest.raises(RCDParseError, match="Missing content braces"):
            RCDParser.parse_content(content)

    def test_parse_content_empty_file(self):
        """Test that parsing fails on empty file."""
        with pytest.raises(RCDParseError, match="Empty file"):
            RCDParser.parse_content("")

    def test_parse_content_missing_name(self):
        """Test that parsing fails when name is missing or only whitespace."""
        # Test with empty first line
        content1 = """
{
//Driver Info
  Nationality=French
}
"""
        with pytest.raises(RCDParseError, match="Missing talent name"):
            RCDParser.parse_content(content1)

        # Test with only spaces
        content2 = """
{
//Driver Info
  Nationality=French
}
"""
        with pytest.raises(RCDParseError, match="Missing talent name"):
            RCDParser.parse_content(content2)

    def test_parse_content_with_defaults(self):
        """Test that missing fields use default values."""
        content = """Test Driver
{
//Driver Info
  Nationality=German

//Driver Stats
  Speed=95.00
}
"""
        talent = RCDParser.parse_content(content)

        # Check defaults for personal info
        assert talent.personal_info.starts == 0
        assert talent.personal_info.poles == 0
        assert talent.personal_info.wins == 0
        assert talent.personal_info.drivers_championships == 0

        # Check defaults for stats (should use TalentStats defaults)
        assert talent.stats.aggression == pytest.approx(50.0)
        assert talent.stats.speed == pytest.approx(95.0)

    def test_parse_file_not_found(self):
        """Test that parsing fails when file doesn't exist."""
        with pytest.raises(RCDParseError):
            RCDParser.parse_file("nonexistent.rcd")

    def test_parse_content_invalid_number(self):
        """Test that parsing fails with invalid number format."""
        content = """Test Driver
{
//Driver Info
  Nationality=German
  Starts=invalid

//Driver Stats
  Speed=95.00
}
"""
        with pytest.raises(RCDParseError, match="Failed to parse personal info"):
            RCDParser.parse_content(content)

    def test_filename_property(self):
        """Test that parsed talent has correct filename property."""
        talent = RCDParser.parse_file(str(BRANDON_LANG_FILE))
        assert talent.filename == "BrandonLang.rcd"
