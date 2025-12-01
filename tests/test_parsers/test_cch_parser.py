"""Tests for CCH Parser."""

import pytest
from pathlib import Path

from src.parsers.cch_parser import CCHParser, CCHParseError
from src.models.championship import Championship


# Test fixtures path
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
SRGP_FILE = FIXTURES_DIR / "SRGrandPrix05.cch"


class TestCCHParser:
    """Test suite for CCHParser."""

    def test_parse_file_srgp(self):
        """Test parsing the SRGrandPrix05 example file."""
        championship = CCHParser.parse_file(str(SRGP_FILE))

        # Check championship object
        assert championship is not None
        assert isinstance(championship, Championship)

        # Check career stats
        assert championship.career is not None
        assert championship.career.experience == 0
        assert championship.career.money == 500

        # Check season
        assert championship.season is not None
        assert championship.season.name == "Rhez Amateur Derby"
        assert championship.season.season_status == 2  # In progress (not completed)
        assert championship.season.gameopt_race_laps == 5
        assert championship.season.gameopt_opponents == 9

        # Check player
        assert championship.player is not None
        assert championship.player.name == "Loic"
        assert championship.player.control_type == 0

        # Check opponents
        assert len(championship.opponents) == 9
        assert championship.opponents[0].name == "Brandon Lang"
        assert championship.opponents[0].opponent_id == 0

        # Check vehicles
        assert len(championship.vehicles) == 3

    def test_parse_career_section(self):
        """Test parsing CAREER section."""
        content = """
[CAREER]
Experience=100
Money=1000
TotalRaces=50
TotalWins=10
"""
        championship = CCHParser.parse_content(content)

        assert championship.career.experience == 100
        assert championship.career.money == 1000
        assert championship.career.total_races == 50
        assert championship.career.total_wins == 10

    def test_parse_vehicle_section(self):
        """Test parsing VEHICLE section."""
        content = """
[VEHICLE]
ID=1
File="GAMEDATA\\VEHICLES\\TEST\\test.veh"
Skin=""
MetersDriven=1000
MoneySpent=500
FreeVehicle=1
Seat=(10.000,10.000)
Mirror=(10.000,10.000)
"""
        championship = CCHParser.parse_content(content)

        assert len(championship.vehicles) == 1
        vehicle = championship.vehicles[0]
        assert vehicle.vehicle_id == 1
        assert "test.veh" in vehicle.file
        assert vehicle.meters_driven == 1000
        assert vehicle.seat == (10.0, 10.0)

    def test_parse_multiple_vehicles(self):
        """Test parsing multiple VEHICLE sections."""
        content = """
[VEHICLE]
ID=0
File="vehicle1.veh"

[VEHICLE]
ID=1
File="vehicle2.veh"

[VEHICLE]
ID=2
File="vehicle3.veh"
"""
        championship = CCHParser.parse_content(content)

        assert len(championship.vehicles) == 3
        assert championship.vehicles[0].vehicle_id == 0
        assert championship.vehicles[1].vehicle_id == 1
        assert championship.vehicles[2].vehicle_id == 2

    def test_parse_season_settings(self):
        """Test parsing CAREERSEASON section."""
        content = """
[CAREERSEASON]
Name="Test Championship"
SeasonStatus=1
CurrentRace=5
GAMEOPT_race_laps=10
GAMEOPT_opponents=15
GAMEOPT_ai_driverstrength=95
"""
        championship = CCHParser.parse_content(content)

        assert championship.season.name == "Test Championship"
        assert championship.season.season_status == 1
        assert championship.season.current_race == 5
        assert championship.season.gameopt_race_laps == 10
        assert championship.season.gameopt_opponents == 15
        assert championship.season.gameopt_ai_driverstrength == 95

    def test_parse_player(self):
        """Test parsing PLAYER section."""
        content = """
[PLAYER]
Name="TestPlayer"
VehFile="test.veh"
RCDFile=""
SeasonPoints=100
PointsPosition=1
PolesTaken=3
OriginalGridPosition=5
CurrentGridPosition=5
Active=1
"""
        championship = CCHParser.parse_content(content)

        assert championship.player is not None
        assert championship.player.name == "TestPlayer"
        assert championship.player.veh_file == "test.veh"
        assert championship.player.season_points == 100
        assert championship.player.points_position == 1
        assert championship.player.control_type == 0

    def test_parse_opponents(self):
        """Test parsing OPPONENT sections."""
        content = """
[OPPONENT00]
Name="Opponent 1"
VehFile="opp1.veh"
SeasonPoints=50

[OPPONENT01]
Name="Opponent 2"
VehFile="opp2.veh"
SeasonPoints=40

[OPPONENT02]
Name="Opponent 3"
VehFile="opp3.veh"
SeasonPoints=30
"""
        championship = CCHParser.parse_content(content)

        assert len(championship.opponents) == 3
        assert championship.opponents[0].name == "Opponent 1"
        assert championship.opponents[0].opponent_id == 0
        assert championship.opponents[1].name == "Opponent 2"
        assert championship.opponents[1].opponent_id == 1
        assert championship.opponents[2].name == "Opponent 3"
        assert championship.opponents[2].opponent_id == 2

    def test_parse_track_stat(self):
        """Test parsing PLAYERTRACKSTAT section."""
        content = """
[PLAYERTRACKSTAT]
TrackName=Mills_Short
TrackFile=GAMEDATA\\LOCATIONS\\Mills\\Mills_Short
ClassRecord="*",0,-1.0000,-1.0000,-1.0000
ClassRecord="GT3",0,-1.0000,-1.0000,-1.0000
"""
        championship = CCHParser.parse_content(content)

        assert len(championship.track_stats) == 1
        track_stat = championship.track_stats[0]
        assert track_stat.track_name == "Mills_Short"
        assert "Mills_Short" in track_stat.track_file

    def test_parse_with_comments(self):
        """Test that comments are ignored."""
        content = """
// This is a comment
[CAREER]
// Another comment
Experience=100
// Comment in the middle
Money=1000
"""
        championship = CCHParser.parse_content(content)

        assert championship.career.experience == 100
        assert championship.career.money == 1000

    def test_parse_empty_values(self):
        """Test parsing with empty values."""
        content = """
[PLAYER]
Name="Test"
VehFile=""
RCDFile=""
"""
        championship = CCHParser.parse_content(content)

        assert championship.player.name == "Test"
        assert championship.player.veh_file == ""
        assert championship.player.rcd_file == ""

    def test_parse_file_not_found(self):
        """Test that parsing fails when file doesn't exist."""
        with pytest.raises(CCHParseError):
            CCHParser.parse_file("nonexistent.cch")

    def test_championship_methods(self):
        """Test Championship helper methods."""
        content = """
[PLAYER]
Name="Player1"
VehFile="p1.veh"

[OPPONENT00]
Name="Opp1"
VehFile="o1.veh"

[OPPONENT01]
Name="Opp2"
VehFile="o2.veh"
Active=0
"""
        championship = CCHParser.parse_content(content)

        # Test get_participant_count
        assert championship.get_participant_count() == 3  # 1 player + 2 opponents

        # Test get_active_opponent_count
        assert championship.get_active_opponent_count() == 1  # Only 1 active

        # Test get_opponent_by_id
        opp = championship.get_opponent_by_id(0)
        assert opp is not None
        assert opp.name == "Opp1"

        # Test get_opponent_by_name
        opp = championship.get_opponent_by_name("Opp2")
        assert opp is not None
        assert opp.opponent_id == 1
