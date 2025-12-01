"""
Parser for rFactor Championship files (.cch).

The .cch format is an extended INI format with:
- Multiple sections with the same name ([VEHICLE])
- Numbered sections ([OPPONENT00], [OPPONENT01], ...)
- Comments with //
- Various data types (int, float, string, tuples)
"""

import re
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path

from ..models.championship import (
    Championship, CareerStats, VehicleEntry, SeasonSettings,
    Player, Opponent, TrackStat
)
from ..utils.file_utils import read_rfactor_file


class CCHParseError(Exception):
    """Exception raised when parsing a CCH file fails."""
    pass


class CCHParser:
    """Parser for .cch (Championship) files."""

    # Regex patterns
    PATTERN_SECTION = re.compile(r'^\[(\w+)\]', re.MULTILINE)
    PATTERN_KEY_VALUE = re.compile(r'^([^=\s]+)\s*=\s*(.*)$')
    PATTERN_TUPLE = re.compile(r'\(([^)]+)\)')

    @staticmethod
    def parse_file(filepath: str) -> Championship:
        """
        Parse a .cch file and return a Championship object.

        Args:
            filepath: Path to the .cch file

        Returns:
            Championship object with parsed data

        Raises:
            CCHParseError: If parsing fails
            FileNotFoundError: If file doesn't exist
        """
        try:
            content = read_rfactor_file(filepath)
            championship = CCHParser.parse_content(content)
            championship.file_path = filepath
            return championship
        except Exception as e:
            raise CCHParseError(f"Failed to parse {filepath}: {e}") from e

    @staticmethod
    def parse_content(content: str) -> Championship:
        """
        Parse the content of a .cch file.

        Args:
            content: Content of the .cch file as string

        Returns:
            Championship object

        Raises:
            CCHParseError: If parsing fails
        """
        # Split content into sections
        sections = CCHParser._split_into_sections(content)

        # Parse each section type
        career = None
        vehicles = []
        season = None
        player = None
        opponents = []
        track_stats = []

        for section_name, section_content in sections:
            if section_name == "CAREER":
                career = CCHParser._parse_career(section_content)
            elif section_name == "VEHICLE":
                vehicle = CCHParser._parse_vehicle(section_content)
                vehicles.append(vehicle)
            elif section_name == "CAREERSEASON":
                season = CCHParser._parse_season(section_content)
            elif section_name == "PLAYER":
                player = CCHParser._parse_player(section_content)
            elif section_name.startswith("OPPONENT"):
                opponent = CCHParser._parse_opponent(section_name, section_content)
                opponents.append(opponent)
            elif section_name == "PLAYERTRACKSTAT":
                track_stat = CCHParser._parse_track_stat(section_content)
                track_stats.append(track_stat)

        # Create championship
        championship = Championship(
            career=career or CareerStats(),
            vehicles=vehicles,
            season=season or SeasonSettings(),
            player=player,
            opponents=opponents,
            track_stats=track_stats,
        )

        return championship

    @staticmethod
    def _split_into_sections(content: str) -> List[Tuple[str, str]]:
        """
        Split content into sections.

        Args:
            content: File content

        Returns:
            List of (section_name, section_content) tuples
        """
        sections = []
        lines = content.split('\n')

        current_section = None
        current_content = []

        for line in lines:
            # Check if line is a section header
            match = CCHParser.PATTERN_SECTION.match(line.strip())
            if match:
                # Save previous section
                if current_section is not None:
                    sections.append((current_section, '\n'.join(current_content)))

                # Start new section
                current_section = match.group(1)
                current_content = []
            elif current_section is not None:
                # Add line to current section
                current_content.append(line)

        # Save last section
        if current_section is not None:
            sections.append((current_section, '\n'.join(current_content)))

        return sections

    @staticmethod
    def _parse_key_value_pairs(content: str) -> Dict[str, str]:
        """
        Parse key=value pairs from content.

        Args:
            content: Content to parse

        Returns:
            Dictionary of key-value pairs
        """
        data = {}
        for line in content.split('\n'):
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                continue

            match = CCHParser.PATTERN_KEY_VALUE.match(line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                data[key] = value

        return data

    @staticmethod
    def _parse_value(value_str: str, value_type: type) -> Any:
        """
        Parse a value string to the specified type.

        Args:
            value_str: String value to parse
            value_type: Type to parse to

        Returns:
            Parsed value
        """
        value_str = value_str.strip().strip('"')

        if value_type == int:
            return int(float(value_str)) if value_str else 0
        elif value_type == float:
            return float(value_str) if value_str else 0.0
        elif value_type == str:
            return value_str
        elif value_type == tuple:
            # Parse tuple like (10.000,10.000)
            match = CCHParser.PATTERN_TUPLE.search(value_str)
            if match:
                values = match.group(1).split(',')
                return tuple(float(v.strip()) for v in values)
            return (0.0, 0.0)
        else:
            return value_str

    @staticmethod
    def _parse_career(content: str) -> CareerStats:
        """Parse [CAREER] section."""
        data = CCHParser._parse_key_value_pairs(content)

        return CareerStats(
            experience=CCHParser._parse_value(data.get('Experience', '0'), int),
            money=CCHParser._parse_value(data.get('Money', '500'), int),
            cur_seas_index=CCHParser._parse_value(data.get('CurSeasIndex', '0'), int),
            single_player_vehicle=CCHParser._parse_value(data.get('SinglePlayerVehicle', ''), str),
            single_player_filter=CCHParser._parse_value(data.get('SinglePlayerFilter', ''), str),
            multi_player_filter=CCHParser._parse_value(data.get('MultiPlayerFilter', ''), str),
            ai_realism=CCHParser._parse_value(data.get('AIRealism', '0.25'), float),
            single_player_ai_strength=CCHParser._parse_value(data.get('SinglePlayerAIStrength', '95'), int),
            multi_player_ai_strength=CCHParser._parse_value(data.get('MultiPlayerAIStrength', '95'), int),
            aborted_seasons=CCHParser._parse_value(data.get('AbortedSeasons', '0'), int),
            total_laps=CCHParser._parse_value(data.get('TotalLaps', '0'), int),
            total_races=CCHParser._parse_value(data.get('TotalRaces', '0'), int),
            total_races_with_ai=CCHParser._parse_value(data.get('TotalRacesWithAI', '0'), int),
            total_points_scored=CCHParser._parse_value(data.get('TotalPointsScored', '0'), int),
            total_championships=CCHParser._parse_value(data.get('TotalChampionships', '0'), int),
            total_wins=CCHParser._parse_value(data.get('TotalWins', '0'), int),
            total_poles=CCHParser._parse_value(data.get('TotalPoles', '0'), int),
            total_lap_records=CCHParser._parse_value(data.get('TotalLapRecords', '0'), int),
            avg_start_position=CCHParser._parse_value(data.get('AvgStartPosition', '0.0'), float),
            avg_finish_position=CCHParser._parse_value(data.get('AvgFinishPosition', '0.0'), float),
            avg_race_distance=CCHParser._parse_value(data.get('AvgRaceDistance', '0.0'), float),
            avg_opponent_strength=CCHParser._parse_value(data.get('AvgOpponentStrength', '0.0'), float),
        )

    @staticmethod
    def _parse_vehicle(content: str) -> VehicleEntry:
        """Parse [VEHICLE] section."""
        data = CCHParser._parse_key_value_pairs(content)

        return VehicleEntry(
            vehicle_id=CCHParser._parse_value(data.get('ID', '0'), int),
            file=CCHParser._parse_value(data.get('File', ''), str),
            skin=CCHParser._parse_value(data.get('Skin', ''), str),
            meters_driven=CCHParser._parse_value(data.get('MetersDriven', '0'), int),
            money_spent=CCHParser._parse_value(data.get('MoneySpent', '0'), int),
            free_vehicle=CCHParser._parse_value(data.get('FreeVehicle', '1'), int),
            seat=CCHParser._parse_value(data.get('Seat', '(10.0,10.0)'), tuple),
            mirror=CCHParser._parse_value(data.get('Mirror', '(10.0,10.0)'), tuple),
            upgrade_list=CCHParser._parse_value(data.get('UpgradeList', ''), str),
        )

    @staticmethod
    def _parse_season(content: str) -> SeasonSettings:
        """Parse [CAREERSEASON] section."""
        data = CCHParser._parse_key_value_pairs(content)

        return SeasonSettings(
            name=CCHParser._parse_value(data.get('Name', 'New Season'), str),
            season_status=CCHParser._parse_value(data.get('SeasonStatus', '0'), int),
            race_session=CCHParser._parse_value(data.get('RaceSession', '0'), int),
            race_over=CCHParser._parse_value(data.get('RaceOver', '0'), int),
            current_race=CCHParser._parse_value(data.get('CurrentRace', '0'), int),
            player_vehicle_id=CCHParser._parse_value(data.get('PlayerVehicleID', '0'), int),
            mechfail_rate=CCHParser._parse_value(data.get('MECHFAIL_rate', '2'), int),
            gameopt_damagemultiplier=CCHParser._parse_value(data.get('GAMEOPT_damagemultiplier', '50'), int),
            gameopt_fuel_mult=CCHParser._parse_value(data.get('GAMEOPT_fuel_mult', '1'), int),
            gameopt_tire_mult=CCHParser._parse_value(data.get('GAMEOPT_tire_mult', '1'), int),
            racecond_reconnaissance=CCHParser._parse_value(data.get('RACECOND_reconnaissance', '0'), int),
            racecond_walkthrough=CCHParser._parse_value(data.get('RACECOND_walkthrough', '1'), int),
            racecond_formation=CCHParser._parse_value(data.get('RACECOND_formation', '3'), int),
            racecond_safetycarcollision=CCHParser._parse_value(data.get('RACECOND_safetycarcollision', '1'), int),
            racecond_safetycar_thresh=CCHParser._parse_value(data.get('RACECOND_safetycar_thresh', '1.0'), float),
            racecond_flag_rules=CCHParser._parse_value(data.get('RACECOND_flag_rules', '2'), int),
            racecond_blue_flags=CCHParser._parse_value(data.get('RACECOND_blue_flags', '7'), int),
            racecond_weather=CCHParser._parse_value(data.get('RACECOND_weather', '0'), int),
            racecond_timescaled_weather=CCHParser._parse_value(data.get('RACECOND_timescaled_weather', '1'), int),
            racecond_race_starting_time=CCHParser._parse_value(data.get('RACECOND_race_starting_time', '840'), int),
            racecond_race_timescale=CCHParser._parse_value(data.get('RACECOND_race_timescale', '1'), int),
            racecond_private_qual=CCHParser._parse_value(data.get('RACECOND_private_qual', '2'), int),
            racecond_parc_ferme=CCHParser._parse_value(data.get('RACECOND_parc_ferme', '3'), int),
            gameopt_ai_driverstrength=CCHParser._parse_value(data.get('GAMEOPT_ai_driverstrength', '95'), int),
            gameopt_free_settings=CCHParser._parse_value(data.get('GAMEOPT_free_settings', '-1'), int),
            gameopt_race_finish_criteria=CCHParser._parse_value(data.get('GAMEOPT_race_finish_criteria', '1'), int),
            gameopt_race_laps=CCHParser._parse_value(data.get('GAMEOPT_race_laps', '5'), int),
            gameopt_race_time=CCHParser._parse_value(data.get('GAMEOPT_race_time', '120'), int),
            gameopt_race_length=CCHParser._parse_value(data.get('GAMEOPT_race_length', '0.1'), float),
            gameopt_opponents=CCHParser._parse_value(data.get('GAMEOPT_opponents', '9'), int),
            gameopt_speed_comp=CCHParser._parse_value(data.get('GAMEOPT_speed_comp', '0'), int),
            gameopt_crash_recovery=CCHParser._parse_value(data.get('GAMEOPT_crash_recovery', '3'), int),
        )

    @staticmethod
    def _parse_player(content: str) -> Player:
        """Parse [PLAYER] section."""
        data = CCHParser._parse_key_value_pairs(content)

        return Player(
            name=CCHParser._parse_value(data.get('Name', 'Player'), str),
            veh_file=CCHParser._parse_value(data.get('VehFile', ''), str),
            rcd_file=CCHParser._parse_value(data.get('RCDFile', ''), str),
            season_points=CCHParser._parse_value(data.get('SeasonPoints', '0'), int),
            points_position=CCHParser._parse_value(data.get('PointsPosition', '0'), int),
            poles_taken=CCHParser._parse_value(data.get('PolesTaken', '0'), int),
            original_grid_position=CCHParser._parse_value(data.get('OriginalGridPosition', '0'), int),
            current_grid_position=CCHParser._parse_value(data.get('CurrentGridPosition', '0'), int),
            control_type=0,  # Player is always 0
            active=CCHParser._parse_value(data.get('Active', '1'), int),
        )

    @staticmethod
    def _parse_opponent(section_name: str, content: str) -> Opponent:
        """Parse [OPPONENTxx] section."""
        data = CCHParser._parse_key_value_pairs(content)

        # Extract opponent ID from section name (OPPONENT00 -> 0)
        opponent_id = 0
        if len(section_name) > 8:  # "OPPONENT" is 8 chars
            try:
                opponent_id = int(section_name[8:])
            except ValueError:
                opponent_id = 0

        return Opponent(
            opponent_id=opponent_id,
            name=CCHParser._parse_value(data.get('Name', f'Opponent {opponent_id}'), str),
            veh_file=CCHParser._parse_value(data.get('VehFile', ''), str),
            rcd_file=CCHParser._parse_value(data.get('RCDFile', ''), str),
            season_points=CCHParser._parse_value(data.get('SeasonPoints', '0'), int),
            points_position=CCHParser._parse_value(data.get('PointsPosition', '0'), int),
            poles_taken=CCHParser._parse_value(data.get('PolesTaken', '0'), int),
            original_grid_position=CCHParser._parse_value(data.get('OriginalGridPosition', '0'), int),
            current_grid_position=CCHParser._parse_value(data.get('CurrentGridPosition', '0'), int),
            control_type=CCHParser._parse_value(data.get('ControlType', '1'), int),
            active=CCHParser._parse_value(data.get('Active', '1'), int),
        )

    @staticmethod
    def _parse_track_stat(content: str) -> TrackStat:
        """Parse [PLAYERTRACKSTAT] section."""
        data = CCHParser._parse_key_value_pairs(content)

        track_stat = TrackStat(
            track_name=CCHParser._parse_value(data.get('TrackName', ''), str),
            track_file=CCHParser._parse_value(data.get('TrackFile', ''), str),
            class_records=[],
        )

        # Parse ClassRecord entries
        for key, value in data.items():
            if key == 'ClassRecord':
                # Parse format: "CLASS",data1,data2,data3
                # For now, just store as raw string
                track_stat.class_records.append(value)

        return track_stat
