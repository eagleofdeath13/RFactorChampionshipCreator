"""Tests for rFactor Validator."""

import pytest
from pathlib import Path

from src.utils.rfactor_validator import RFactorValidator, RFactorValidationError


# Use the actual RFactorFiles directory for testing
RFACTOR_TEST_PATH = Path(__file__).parent.parent.parent / "RFactorFiles"


class TestRFactorValidator:
    """Test suite for RFactorValidator."""

    def test_validate_valid_installation(self):
        """Test validation of a valid rFactor installation."""
        if not RFACTOR_TEST_PATH.exists():
            pytest.skip("RFactorFiles directory not available")

        is_valid, missing = RFactorValidator.validate(str(RFACTOR_TEST_PATH))

        assert is_valid is True
        assert len(missing) == 0

    def test_validate_invalid_path_not_exists(self):
        """Test validation of non-existent path."""
        is_valid, missing = RFactorValidator.validate("C:/NonExistent/Path")

        assert is_valid is False
        assert "Directory does not exist" in missing

    def test_validate_invalid_path_is_file(self, tmp_path):
        """Test validation when path is a file, not a directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        is_valid, missing = RFactorValidator.validate(str(test_file))

        assert is_valid is False
        assert "Path is not a directory" in missing

    def test_validate_missing_required_items(self, tmp_path):
        """Test validation with missing required items."""
        # Create empty directory
        test_dir = tmp_path / "rfactor"
        test_dir.mkdir()

        is_valid, missing = RFactorValidator.validate(str(test_dir))

        assert is_valid is False
        assert "rFactor.exe" in missing
        assert "GameData" in missing
        assert "UserData" in missing

    def test_validate_or_raise_valid(self):
        """Test validate_or_raise with valid installation."""
        if not RFACTOR_TEST_PATH.exists():
            pytest.skip("RFactorFiles directory not available")

        # Should not raise
        RFactorValidator.validate_or_raise(str(RFACTOR_TEST_PATH))

    def test_validate_or_raise_invalid(self):
        """Test validate_or_raise with invalid path."""
        with pytest.raises(RFactorValidationError, match="Invalid rFactor installation"):
            RFactorValidator.validate_or_raise("C:/NonExistent/Path")

    def test_get_version_info(self):
        """Test getting version info from installation."""
        if not RFACTOR_TEST_PATH.exists():
            pytest.skip("RFactorFiles directory not available")

        info = RFactorValidator.get_version_info(str(RFACTOR_TEST_PATH))

        assert "path" in info
        assert "exists" in info
        assert "is_valid" in info
        assert info["is_valid"] is True
        assert "talent_count" in info
        assert info["talent_count"] > 0  # Should have some talents

    def test_get_version_info_invalid_path(self):
        """Test getting version info from invalid path."""
        info = RFactorValidator.get_version_info("C:/NonExistent")

        assert info["exists"] is False
        assert info["is_valid"] is False
        assert "talent_count" not in info

    def test_find_user_data_dir(self):
        """Test finding UserData directory."""
        if not RFACTOR_TEST_PATH.exists():
            pytest.skip("RFactorFiles directory not available")

        userdata_path = RFactorValidator.find_user_data_dir(str(RFACTOR_TEST_PATH))

        assert userdata_path.exists()
        assert userdata_path.is_dir()
        assert userdata_path.name == "UserData"

    def test_find_user_data_dir_not_exists(self, tmp_path):
        """Test finding UserData when it doesn't exist."""
        with pytest.raises(RFactorValidationError, match="UserData directory not found"):
            RFactorValidator.find_user_data_dir(str(tmp_path))

    def test_list_player_profiles(self):
        """Test listing player profiles."""
        if not RFACTOR_TEST_PATH.exists():
            pytest.skip("RFactorFiles directory not available")

        profiles = RFactorValidator.list_player_profiles(str(RFACTOR_TEST_PATH))

        assert isinstance(profiles, list)
        # Should have at least one profile (Loic)
        assert len(profiles) > 0
        assert "Loic" in profiles

    def test_list_player_profiles_empty(self, tmp_path):
        """Test listing profiles when UserData is empty."""
        # Create UserData directory
        userdata = tmp_path / "UserData"
        userdata.mkdir()

        profiles = RFactorValidator.list_player_profiles(str(tmp_path))

        assert isinstance(profiles, list)
        assert len(profiles) == 0
