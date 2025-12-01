"""
Parser for rFactor RFM (RFactor Mod) files.

RFM files define championships with seasons, scoring, and configuration.
"""

import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple

from ..models.rfm import (
    RFMod,
    Season,
    DefaultScoring,
    SeasonScoringInfo,
    PitGroup,
    CareerSettings,
)


class RFMParser:
    """Parser for RFM files."""

    def __init__(self, file_path: str):
        """
        Initialize parser.

        Args:
            file_path: Path to RFM file
        """
        self.file_path = Path(file_path)
        self.lines: List[str] = []
        self.current_line: int = 0

    def parse(self) -> RFMod:
        """
        Parse RFM file.

        Returns:
            RFMod object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"RFM file not found: {self.file_path}")

        # Read file with proper encoding
        with open(self.file_path, 'r', encoding='windows-1252') as f:
            self.lines = f.readlines()

        self.current_line = 0

        # Initialize with defaults
        mod_name = ""
        vehicle_filter = ""
        track_filter = "*"
        safety_car = "Hammer_PC.veh"
        max_opponents = 19
        min_championship_opponents = 3

        # Optional fields
        matchmaker = "match.rfactor.net"
        matchmaker_tcp_port = 39001
        matchmaker_udp_port = 39002
        racecast_location = "racecast.rfactor.net"
        loading_bar_color = 16750848

        seasons: List[Season] = []
        default_scoring = DefaultScoring()
        season_scoring_info = SeasonScoringInfo()
        career_settings = CareerSettings()
        scene_order: List[str] = []
        pit_group_order: List[PitGroup] = []
        pit_order_by_qualifying = False
        config_overrides: Dict[str, str] = {}

        # Parse file
        while self.current_line < len(self.lines):
            line = self._get_clean_line()

            if not line:
                self.current_line += 1
                continue

            # Check for sections
            if line.startswith("Season =") or line.startswith("Season="):
                season = self._parse_season(line)
                seasons.append(season)

            elif line.startswith("DefaultScoring"):
                default_scoring = self._parse_default_scoring()

            elif line.startswith("SeasonScoringInfo"):
                season_scoring_info = self._parse_season_scoring_info()

            elif line.startswith("SceneOrder"):
                # Global scene order
                scene_order = self._parse_scene_order()

            elif line.startswith("PitGroupOrder"):
                pit_group_order = self._parse_pit_group_order()

            elif line.startswith("ConfigOverrides"):
                config_overrides = self._parse_config_overrides()

            elif "=" in line:
                # Parse key-value pairs
                key, value = self._parse_key_value(line)

                if key == "Mod Name":
                    mod_name = value
                elif key == "Vehicle Filter":
                    vehicle_filter = value
                elif key == "Track Filter":
                    track_filter = value
                elif key == "SafetyCar":
                    safety_car = value
                elif key == "Max Opponents":
                    max_opponents = int(value)
                elif key == "Min Championship Opponents":
                    min_championship_opponents = int(value)
                elif key == "Matchmaker":
                    matchmaker = value
                elif key == "Matchmaker TCP Port":
                    matchmaker_tcp_port = int(value)
                elif key == "Matchmaker UDP Port":
                    matchmaker_udp_port = int(value)
                elif key == "RaceCast Location":
                    racecast_location = value
                elif key == "Loading Bar Color":
                    loading_bar_color = int(value)
                elif key == "PitOrderByQualifying":
                    pit_order_by_qualifying = value.lower() in ('true', '1', 'yes')

                # Career settings
                elif key == "StartingMoney":
                    career_settings.starting_money = int(value)
                elif key == "StartingExperience":
                    career_settings.starting_experience = int(value)
                elif key == "StartingVehicle":
                    # Can appear multiple times, split by comma if multiple values
                    vehicles = [v.strip() for v in value.split(',')]
                    career_settings.starting_vehicles.extend(vehicles)
                elif key == "DriveAnyUnlocked":
                    career_settings.drive_any_unlocked = int(value)

                # Multipliers
                elif key == "BaseCreditMult":
                    career_settings.base_credit_mult = float(value)
                elif key == "LapMoneyMult":
                    career_settings.lap_money_mult = float(value)
                elif key == "LapExpMult":
                    career_settings.lap_exp_mult = float(value)
                elif key == "FineMoneyMult":
                    career_settings.fine_money_mult = float(value)
                elif key == "FineExpMult":
                    career_settings.fine_exp_mult = float(value)
                elif key == "PoleSingleMoneyMult":
                    career_settings.pole_single_money_mult = float(value)
                elif key == "PoleSingleExpMult":
                    career_settings.pole_single_exp_mult = float(value)
                elif key == "PoleCareerMoneyMult":
                    career_settings.pole_career_money_mult = float(value)
                elif key == "PoleCareerExpMult":
                    career_settings.pole_career_exp_mult = float(value)
                elif key == "PoleMultiMoneyMult":
                    career_settings.pole_multi_money_mult = float(value)
                elif key == "PoleMultiExpMult":
                    career_settings.pole_multi_exp_mult = float(value)
                elif key == "WinSingleMoneyMult":
                    career_settings.win_single_money_mult = float(value)
                elif key == "WinSingleExpMult":
                    career_settings.win_single_exp_mult = float(value)
                elif key == "WinCareerMoneyMult":
                    career_settings.win_career_money_mult = float(value)
                elif key == "WinCareerExpMult":
                    career_settings.win_career_exp_mult = float(value)
                elif key == "WinMultiMoneyMult":
                    career_settings.win_multi_money_mult = float(value)
                elif key == "WinMultiExpMult":
                    career_settings.win_multi_exp_mult = float(value)
                elif key == "PointsSingleMoneyMult":
                    career_settings.points_single_money_mult = float(value)
                elif key == "PointsSingleExpMult":
                    career_settings.points_single_exp_mult = float(value)
                elif key == "PointsCareerMoneyMult":
                    career_settings.points_career_money_mult = float(value)
                elif key == "PointsCareerExpMult":
                    career_settings.points_career_exp_mult = float(value)
                elif key == "PointsMultiMoneyMult":
                    career_settings.points_multi_money_mult = float(value)
                elif key == "PointsMultiExpMult":
                    career_settings.points_multi_exp_mult = float(value)

            self.current_line += 1

        # Validate required fields
        if not mod_name:
            raise ValueError("Missing required field: Mod Name")

        # Create RFMod object
        rfm = RFMod(
            mod_name=mod_name,
            vehicle_filter=vehicle_filter,
            track_filter=track_filter,
            safety_car=safety_car,
            max_opponents=max_opponents,
            min_championship_opponents=min_championship_opponents,
            seasons=seasons,
            default_scoring=default_scoring,
            season_scoring_info=season_scoring_info,
            career_settings=career_settings,
            scene_order=scene_order,
            pit_order_by_qualifying=pit_order_by_qualifying,
            pit_group_order=pit_group_order,
            matchmaker=matchmaker,
            matchmaker_tcp_port=matchmaker_tcp_port,
            matchmaker_udp_port=matchmaker_udp_port,
            racecast_location=racecast_location,
            loading_bar_color=loading_bar_color,
            config_overrides=config_overrides,
            file_path=str(self.file_path)
        )

        return rfm

    def _get_clean_line(self) -> str:
        """Get current line without comments and whitespace."""
        if self.current_line >= len(self.lines):
            return ""

        line = self.lines[self.current_line]

        # Remove comments
        comment_pos = line.find('//')
        if comment_pos != -1:
            line = line[:comment_pos]

        return line.strip()

    def _parse_key_value(self, line: str) -> Tuple[str, str]:
        """Parse key = value line."""
        parts = line.split('=', 1)
        if len(parts) != 2:
            return "", ""

        key = parts[0].strip()
        value = parts[1].strip()

        return key, value

    def _parse_season(self, declaration_line: str) -> Season:
        """Parse a Season {...} block."""
        # Extract season name
        match = re.match(r'Season\s*=\s*(.+)', declaration_line)
        if not match:
            raise ValueError(f"Invalid Season declaration at line {self.current_line + 1}")

        season_name = match.group(1).strip()
        self.current_line += 1

        # Find opening brace
        while self.current_line < len(self.lines):
            line = self._get_clean_line()
            if '{' in line:
                self.current_line += 1
                break
            self.current_line += 1

        # Parse season content
        vehicle_filter = ""
        min_championship_opponents = 5
        full_season_name = None
        min_experience = None
        entry_fee = None
        scene_order: List[str] = []

        while self.current_line < len(self.lines):
            line = self._get_clean_line()

            if '}' in line:
                break

            if line.startswith("SceneOrder"):
                scene_order = self._parse_scene_order()
            elif "=" in line:
                key, value = self._parse_key_value(line)

                if key == "Vehicle Filter":
                    vehicle_filter = value
                elif key == "Min Championship Opponents":
                    min_championship_opponents = int(value)
                elif key == "FullSeasonName":
                    full_season_name = value
                elif key == "MinExperience":
                    min_experience = int(value)
                elif key == "EntryFee":
                    entry_fee = int(value)

            self.current_line += 1

        return Season(
            name=season_name,
            vehicle_filter=vehicle_filter,
            scene_order=scene_order,
            min_championship_opponents=min_championship_opponents,
            full_season_name=full_season_name,
            min_experience=min_experience,
            entry_fee=entry_fee
        )

    def _parse_scene_order(self) -> List[str]:
        """Parse a SceneOrder {...} block."""
        self.current_line += 1

        # Find opening brace
        while self.current_line < len(self.lines):
            line = self._get_clean_line()
            if '{' in line:
                self.current_line += 1
                break
            self.current_line += 1

        scenes: List[str] = []

        while self.current_line < len(self.lines):
            line = self._get_clean_line()

            if '}' in line:
                break

            if line:
                scenes.append(line)

            self.current_line += 1

        return scenes

    def _parse_default_scoring(self) -> DefaultScoring:
        """Parse DefaultScoring {...} block."""
        self.current_line += 1

        # Find opening brace
        while self.current_line < len(self.lines):
            line = self._get_clean_line()
            if '{' in line:
                self.current_line += 1
                break
            self.current_line += 1

        scoring = DefaultScoring()

        while self.current_line < len(self.lines):
            line = self._get_clean_line()

            if '}' in line:
                break

            if "=" in line:
                key, value = self._parse_key_value(line)

                if key == "RacePitKPH":
                    scoring.race_pit_kph = int(value)
                elif key == "NormalPitKPH":
                    scoring.normal_pit_kph = int(value)
                elif key == "Practice1Day":
                    scoring.practice1_day = value
                elif key == "Practice1Start":
                    scoring.practice1_start = value
                elif key == "Practice1Duration":
                    scoring.practice1_duration = int(value)
                elif key == "Practice2Day":
                    scoring.practice2_day = value
                elif key == "Practice2Start":
                    scoring.practice2_start = value
                elif key == "Practice2Duration":
                    scoring.practice2_duration = int(value)
                elif key == "Practice3Day":
                    scoring.practice3_day = value
                elif key == "Practice3Start":
                    scoring.practice3_start = value
                elif key == "Practice3Duration":
                    scoring.practice3_duration = int(value)
                elif key == "Practice4Day":
                    scoring.practice4_day = value
                elif key == "Practice4Start":
                    scoring.practice4_start = value
                elif key == "Practice4Duration":
                    scoring.practice4_duration = int(value)
                elif key == "QualifyDay":
                    scoring.qualify_day = value
                elif key == "QualifyStart":
                    scoring.qualify_start = value
                elif key == "QualifyDuration":
                    scoring.qualify_duration = int(value)
                elif key == "QualifyLaps":
                    scoring.qualify_laps = int(value)
                elif key == "WarmupDay":
                    scoring.warmup_day = value
                elif key == "WarmupStart":
                    scoring.warmup_start = value
                elif key == "WarmupDuration":
                    scoring.warmup_duration = int(value)
                elif key == "RaceDay":
                    scoring.race_day = value
                elif key == "RaceStart":
                    scoring.race_start = value
                elif key == "RaceLaps":
                    scoring.race_laps = int(value)
                elif key == "RaceTime":
                    scoring.race_time = int(value)

            self.current_line += 1

        return scoring

    def _parse_season_scoring_info(self) -> SeasonScoringInfo:
        """Parse SeasonScoringInfo {...} block."""
        self.current_line += 1

        # Find opening brace
        while self.current_line < len(self.lines):
            line = self._get_clean_line()
            if '{' in line:
                self.current_line += 1
                break
            self.current_line += 1

        scoring = SeasonScoringInfo()

        while self.current_line < len(self.lines):
            line = self._get_clean_line()

            if '}' in line:
                break

            if "=" in line:
                key, value = self._parse_key_value(line)

                if key == "FirstPlace":
                    scoring.first_place = int(value)
                elif key == "SecondPlace":
                    scoring.second_place = int(value)
                elif key == "ThirdPlace":
                    scoring.third_place = int(value)
                elif key == "FourthPlace":
                    scoring.fourth_place = int(value)
                elif key == "FifthPlace":
                    scoring.fifth_place = int(value)
                elif key == "SixthPlace":
                    scoring.sixth_place = int(value)
                elif key == "SeventhPlace":
                    scoring.seventh_place = int(value)
                elif key == "EighthPlace":
                    scoring.eighth_place = int(value)

            self.current_line += 1

        return scoring

    def _parse_pit_group_order(self) -> List[PitGroup]:
        """Parse PitGroupOrder {...} block."""
        self.current_line += 1

        # Find opening brace
        while self.current_line < len(self.lines):
            line = self._get_clean_line()
            if '{' in line:
                self.current_line += 1
                break
            self.current_line += 1

        pit_groups: List[PitGroup] = []

        while self.current_line < len(self.lines):
            line = self._get_clean_line()

            if '}' in line:
                break

            if "=" in line:
                key, value = self._parse_key_value(line)

                if key == "PitGroup":
                    # Format: PitGroup = 1, Group1
                    parts = [p.strip() for p in value.split(',')]
                    if len(parts) == 2:
                        num_vehicles = int(parts[0])
                        group_name = parts[1]
                        pit_groups.append(PitGroup(num_vehicles, group_name))

            self.current_line += 1

        return pit_groups

    def _parse_config_overrides(self) -> Dict[str, str]:
        """Parse ConfigOverrides {...} block."""
        self.current_line += 1

        # Find opening brace
        while self.current_line < len(self.lines):
            line = self._get_clean_line()
            if '{' in line:
                self.current_line += 1
                break
            self.current_line += 1

        overrides: Dict[str, str] = {}

        while self.current_line < len(self.lines):
            line = self._get_clean_line()

            if '}' in line:
                break

            if "=" in line:
                key, value = self._parse_key_value(line)
                overrides[key] = value

            self.current_line += 1

        return overrides


def parse_rfm(file_path: str) -> RFMod:
    """
    Parse an RFM file.

    Args:
        file_path: Path to RFM file

    Returns:
        RFMod object

    Example:
        >>> rfm = parse_rfm("path/to/SRGrandPrix05.rfm")
        >>> print(rfm.mod_name)
        SR Grand Prix Season
    """
    parser = RFMParser(file_path)
    return parser.parse()
