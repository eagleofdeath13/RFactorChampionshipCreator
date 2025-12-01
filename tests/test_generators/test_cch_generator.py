"""Tests for CCH Generator."""

import pytest
from pathlib import Path
import tempfile
import os

from src.generators.cch_generator import CCHGenerator
from src.parsers.cch_parser import CCHParser
from src.models.championship import (
    Championship, CareerStats, VehicleEntry, SeasonSettings,
    Player, Opponent, TrackStat
)


# Test fixtures path
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
SRGP_FILE = FIXTURES_DIR / "SRGrandPrix05.cch"


class TestCCHGenerator:
    """Test suite for CCHGenerator."""

    def test_to_content_basic(self):
        """Test generating content from a basic Championship object."""
        career = CareerStats(
            experience=100,
            money=1000,
            total_races=10,
        )

        season = SeasonSettings(
            name="Test Championship",
            season_status=1,
            gameopt_race_laps=10,
        )

        player = Player(
            name="TestPlayer",
            veh_file="test.veh",
        )

        championship = Championship(
            career=career,
            season=season,
            player=player,
        )

        content = CCHGenerator.to_content(championship)

        # Check that content contains expected elements
        assert "[CAREER]" in content
        assert "Experience=100" in content
        assert "[CAREERSEASON]" in content
        assert 'Name="Test Championship"' in content
        assert "[PLAYER]" in content
        assert 'Name="TestPlayer"' in content

    def test_generate_and_read_back(self):
        """Test round-trip: generate file and parse it back."""
        # Create a championship
        career = CareerStats(
            experience=50,
            money=750,
            total_wins=5,
        )

        vehicle = VehicleEntry(
            vehicle_id=0,
            file="test_vehicle.veh",
            meters_driven=1000,
        )

        season = SeasonSettings(
            name="Round Trip Test",
            season_status=1,
            gameopt_opponents=5,
        )

        player = Player(
            name="Player1",
            veh_file="player.veh",
            season_points=100,
        )

        opponent = Opponent(
            opponent_id=0,
            name="Opponent1",
            veh_file="opp.veh",
            season_points=80,
        )

        championship = Championship(
            career=career,
            vehicles=[vehicle],
            season=season,
            player=player,
            opponents=[opponent],
        )

        # Generate file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cch', delete=False, encoding='cp1252') as f:
            temp_file = f.name

        try:
            CCHGenerator.generate(championship, temp_file)

            # Parse it back
            parsed = CCHParser.parse_file(temp_file)

            # Compare
            assert parsed.career.experience == championship.career.experience
            assert parsed.career.money == championship.career.money
            assert parsed.season.name == championship.season.name
            assert parsed.player.name == championship.player.name
            assert len(parsed.opponents) == len(championship.opponents)
            assert parsed.opponents[0].name == championship.opponents[0].name

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_round_trip_with_real_file(self):
        """Test round-trip with the real SRGrandPrix05 file."""
        if not SRGP_FILE.exists():
            pytest.skip("SRGrandPrix05.cch not available")

        # Parse original
        original = CCHParser.parse_file(str(SRGP_FILE))

        # Generate to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cch', delete=False, encoding='cp1252') as f:
            temp_file = f.name

        try:
            CCHGenerator.generate(original, temp_file)

            # Parse generated file
            regenerated = CCHParser.parse_file(temp_file)

            # Compare career stats
            assert regenerated.career.experience == original.career.experience
            assert regenerated.career.money == original.career.money
            assert regenerated.career.total_races == original.career.total_races

            # Compare season
            assert regenerated.season.name == original.season.name
            assert regenerated.season.season_status == original.season.season_status
            assert regenerated.season.gameopt_race_laps == original.season.gameopt_race_laps
            assert regenerated.season.gameopt_opponents == original.season.gameopt_opponents

            # Compare player
            assert regenerated.player.name == original.player.name
            assert regenerated.player.veh_file == original.player.veh_file
            assert regenerated.player.season_points == original.player.season_points

            # Compare opponents
            assert len(regenerated.opponents) == len(original.opponents)
            for i, (regen_opp, orig_opp) in enumerate(zip(regenerated.opponents, original.opponents)):
                assert regen_opp.name == orig_opp.name, f"Opponent {i} name mismatch"
                assert regen_opp.veh_file == orig_opp.veh_file, f"Opponent {i} vehicle mismatch"

            # Compare vehicles
            assert len(regenerated.vehicles) == len(original.vehicles)

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_generate_multiple_opponents(self):
        """Test generating with multiple opponents."""
        season = SeasonSettings(name="Multi Opponent Test")
        player = Player(name="Player", veh_file="p.veh")

        opponents = [
            Opponent(opponent_id=0, name="Opp1", veh_file="o1.veh"),
            Opponent(opponent_id=1, name="Opp2", veh_file="o2.veh"),
            Opponent(opponent_id=2, name="Opp3", veh_file="o3.veh"),
        ]

        championship = Championship(
            season=season,
            player=player,
            opponents=opponents,
        )

        content = CCHGenerator.to_content(championship)

        # Check opponent sections are correctly formatted
        assert "[OPPONENT00]" in content
        assert "[OPPONENT01]" in content
        assert "[OPPONENT02]" in content
        assert 'Name="Opp1"' in content
        assert 'Name="Opp2"' in content
        assert 'Name="Opp3"' in content

    def test_generate_with_track_stats(self):
        """Test generating with track statistics."""
        season = SeasonSettings(name="Track Stats Test")
        player = Player(name="Player", veh_file="p.veh")

        track_stat = TrackStat(
            track_name="TestTrack",
            track_file="GAMEDATA\\LOCATIONS\\Test\\test.gdb",
            class_records=['"*",0,-1.0000,-1.0000,-1.0000'],
        )

        championship = Championship(
            season=season,
            player=player,
            track_stats=[track_stat],
        )

        content = CCHGenerator.to_content(championship)

        assert "[PLAYERTRACKSTAT]" in content
        assert "TrackName=TestTrack" in content
        assert "ClassRecord=" in content

    def test_generate_formats_floats_correctly(self):
        """Test that floats are formatted with correct precision."""
        career = CareerStats(
            ai_realism=0.25,
            avg_start_position=5.123456,
        )

        season = SeasonSettings(
            racecond_safetycar_thresh=1.0,
            gameopt_race_length=0.1,
        )

        championship = Championship(
            career=career,
            season=season,
        )

        content = CCHGenerator.to_content(championship)

        # Check float formatting
        assert "AIRealism=0.2500" in content
        assert "AvgStartPosition=5.123456" in content
        assert "RACECOND_safetycar_thresh=1.000000" in content

    def test_generate_creates_directories(self):
        """Test that generator creates parent directories if needed."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create path with non-existent subdirectories
            filepath = Path(temp_dir) / "subdir1" / "subdir2" / "test.cch"

            season = SeasonSettings(name="Test")
            player = Player(name="Test", veh_file="test.veh")
            championship = Championship(season=season, player=player)

            # Should not raise an error
            CCHGenerator.generate(championship, str(filepath))

            # Check file was created
            assert filepath.exists()

    def test_generate_with_empty_strings(self):
        """Test generating with empty string values."""
        player = Player(
            name="Test",
            veh_file="",
            rcd_file="",
        )

        championship = Championship(player=player)
        content = CCHGenerator.to_content(championship)

        assert 'VehFile=""' in content
        assert 'RCDFile=""' in content

    def test_vehicle_tuple_formatting(self):
        """Test that vehicle seat/mirror tuples are formatted correctly."""
        vehicle = VehicleEntry(
            vehicle_id=0,
            file="test.veh",
            seat=(10.5, 12.75),
            mirror=(8.25, 9.5),
        )

        championship = Championship(vehicles=[vehicle])
        content = CCHGenerator.to_content(championship)

        assert "Seat=(10.500,12.750)" in content
        assert "Mirror=(8.250,9.500)" in content
