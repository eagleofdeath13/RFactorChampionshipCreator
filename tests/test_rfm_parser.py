"""
Tests for RFM parser and generator.
"""

import pytest
import tempfile
import os
from pathlib import Path

from src.parsers.rfm_parser import parse_rfm, RFMParser
from src.generators.rfm_generator import generate_rfm
from src.models.rfm import RFMod, Season, DefaultScoring, SeasonScoringInfo, PitGroup


class TestRFMParser:
    """Tests for RFM parser."""

    @pytest.fixture
    def sample_rfm_file(self):
        """Get path to a sample RFM file."""
        # Use one of the existing RFM files in the project
        rfm_path = Path("RFactorFiles/rFm/SRGrandPrix05.rfm")
        if rfm_path.exists():
            return str(rfm_path)
        pytest.skip("Sample RFM file not found")

    def test_parse_rfm_file(self, sample_rfm_file):
        """Test parsing an actual RFM file."""
        rfm = parse_rfm(sample_rfm_file)

        assert rfm is not None
        assert rfm.mod_name == "SR Grand Prix Season"
        assert len(rfm.seasons) == 8
        assert rfm.max_opponents == 19
        assert rfm.min_championship_opponents == 3

    def test_parse_rfm_seasons(self, sample_rfm_file):
        """Test that seasons are parsed correctly."""
        rfm = parse_rfm(sample_rfm_file)

        # Check first season
        first_season = rfm.seasons[0]
        assert first_season.name == "Rhez Amateur Derby"
        assert first_season.vehicle_filter == "GT3"
        assert len(first_season.scene_order) == 3
        assert "Mills_Short" in first_season.scene_order

    def test_parse_rfm_scoring(self, sample_rfm_file):
        """Test that scoring is parsed correctly."""
        rfm = parse_rfm(sample_rfm_file)

        # Check default scoring
        assert rfm.default_scoring.race_pit_kph == 80
        assert rfm.default_scoring.race_laps == 50
        assert rfm.default_scoring.race_time == 120

        # Check season scoring
        assert rfm.season_scoring_info.first_place == 10
        assert rfm.season_scoring_info.second_place == 8

    def test_parse_nonexistent_file(self):
        """Test parsing a nonexistent file."""
        with pytest.raises(FileNotFoundError):
            parse_rfm("nonexistent_file.rfm")


class TestRFMGenerator:
    """Tests for RFM generator."""

    def test_generate_simple_rfm(self):
        """Test generating a simple RFM file."""
        # Create a minimal RFMod
        rfm = RFMod(
            mod_name="Test Championship",
            vehicle_filter="RFTOOL_TestChamp",
            track_filter="*",
        )

        # Add a season
        season = Season(
            name="Test Season",
            vehicle_filter="RFTOOL_TestChamp",
            scene_order=["Mills_Short", "Toban_Long"],
        )
        rfm.add_season(season)

        # Generate to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rfm') as f:
            temp_path = f.name

        try:
            generate_rfm(rfm, temp_path)

            # Check file was created
            assert os.path.exists(temp_path)

            # Check file content
            with open(temp_path, 'r', encoding='windows-1252') as f:
                content = f.read()
                assert "Test Championship" in content
                assert "RFTOOL_TestChamp" in content
                assert "Mills_Short" in content

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_round_trip(self, sample_rfm_file="RFactorFiles/rFm/SRGrandPrix05.rfm"):
        """Test parse → generate → parse round-trip."""
        if not Path(sample_rfm_file).exists():
            pytest.skip("Sample RFM file not found")

        # Parse original
        rfm1 = parse_rfm(sample_rfm_file)

        # Generate to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rfm') as f:
            temp_path = f.name

        try:
            generate_rfm(rfm1, temp_path)

            # Parse generated file
            rfm2 = parse_rfm(temp_path)

            # Compare key attributes
            assert rfm1.mod_name == rfm2.mod_name
            assert len(rfm1.seasons) == len(rfm2.seasons)
            assert rfm1.max_opponents == rfm2.max_opponents
            assert rfm1.season_scoring_info.first_place == rfm2.season_scoring_info.first_place

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_generate_with_all_features(self):
        """Test generating an RFM with all features."""
        rfm = RFMod(
            mod_name="Complete Test",
            vehicle_filter="RFTOOL_Complete",
            track_filter="SRGrandPrix",
            max_opponents=15,
            min_championship_opponents=5,
        )

        # Add season with all options
        season = Season(
            name="Full Season",
            vehicle_filter="RFTOOL_Complete",
            scene_order=["Mills_Short", "Toban_Long", "Joesville_Speedway"],
            min_championship_opponents=5,
            full_season_name="Complete Full Season Name",
            min_experience=1000,
            entry_fee=500,
        )
        rfm.add_season(season)

        # Add pit groups
        rfm.pit_group_order = [
            PitGroup(1, "Group1"),
            PitGroup(1, "Group2"),
        ]

        # Generate
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rfm') as f:
            temp_path = f.name

        try:
            generate_rfm(rfm, temp_path)

            # Parse back
            rfm2 = parse_rfm(temp_path)

            assert rfm2.mod_name == "Complete Test"
            assert len(rfm2.seasons) == 1
            assert rfm2.seasons[0].min_experience == 1000
            assert rfm2.seasons[0].entry_fee == 500
            assert len(rfm2.pit_group_order) == 2

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
