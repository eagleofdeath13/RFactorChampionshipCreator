"""
Parser for rFactor Talent files (.rcd).

Format example:
    Brandon Lang
    {
    //Driver Info
      Nationality=American
      DateofBirth=28-11-1984
      Starts=9
      Poles=2
      Wins=0
      DriversChampionships=0

    //Driver Stats
      Aggression=74.73
      Reputation=57.89
      ...
    }
"""

import re
from typing import Dict, Tuple
from pathlib import Path

from ..models.talent import Talent, TalentPersonalInfo, TalentStats
from ..utils.file_utils import read_rfactor_file


class RCDParseError(Exception):
    """Exception raised when parsing an RCD file fails."""
    pass


class RCDParser:
    """Parser for .rcd (Talent) files."""

    # Regex patterns
    PATTERN_NAME = re.compile(r'^(.+?)$', re.MULTILINE)
    PATTERN_CONTENT = re.compile(r'\{(.+?)\}', re.DOTALL)
    PATTERN_KEY_VALUE = re.compile(r'^\s*(\w+)\s*=\s*(.+?)\s*$', re.MULTILINE)

    @staticmethod
    def parse_file(filepath: str) -> Talent:
        """
        Parse a .rcd file and return a Talent object.

        Args:
            filepath: Path to the .rcd file

        Returns:
            Talent object with parsed data

        Raises:
            RCDParseError: If parsing fails
            FileNotFoundError: If file doesn't exist
        """
        try:
            content = read_rfactor_file(filepath)
            talent = RCDParser.parse_content(content)
            talent.file_path = filepath
            return talent
        except Exception as e:
            raise RCDParseError(f"Failed to parse {filepath}: {e}") from e

    @staticmethod
    def parse_content(content: str) -> Talent:
        """
        Parse the content of a .rcd file.

        Args:
            content: Content of the .rcd file as string

        Returns:
            Talent object

        Raises:
            RCDParseError: If parsing fails
        """
        # Check if content is empty
        if not content or not content.strip():
            raise RCDParseError("Empty file")

        # Extract name (first non-empty line before braces, not containing =)
        lines = content.strip().split('\n')
        name = None
        for line in lines:
            stripped = line.strip()
            # Name should not be a comment, not be braces, and not contain =
            if (stripped and
                not stripped.startswith('//') and
                not stripped.startswith('{') and
                stripped not in ('{', '}') and
                '=' not in stripped):
                name = stripped
                break

        if not name:
            raise RCDParseError("Missing talent name")

        # Extract content between braces
        match = RCDParser.PATTERN_CONTENT.search(content)
        if not match:
            raise RCDParseError("Missing content braces { }")

        brace_content = match.group(1)

        # Parse key-value pairs
        data = RCDParser._parse_key_value_pairs(brace_content)

        # Create personal info
        personal_info = RCDParser._create_personal_info(data)

        # Create stats
        stats = RCDParser._create_stats(data)

        return Talent(
            name=name,
            personal_info=personal_info,
            stats=stats,
        )

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
        for match in RCDParser.PATTERN_KEY_VALUE.finditer(content):
            key = match.group(1).strip()
            value = match.group(2).strip()
            data[key] = value
        return data

    @staticmethod
    def _create_personal_info(data: Dict[str, str]) -> TalentPersonalInfo:
        """
        Create TalentPersonalInfo from parsed data.

        Args:
            data: Parsed key-value pairs

        Returns:
            TalentPersonalInfo object

        Raises:
            RCDParseError: If required fields are missing
        """
        try:
            return TalentPersonalInfo(
                nationality=data.get('Nationality', 'Unknown'),
                date_of_birth=data.get('DateofBirth', '01-01-1980'),
                starts=int(data.get('Starts', 0)),
                poles=int(data.get('Poles', 0)),
                wins=int(data.get('Wins', 0)),
                drivers_championships=int(data.get('DriversChampionships', 0)),
            )
        except (ValueError, KeyError) as e:
            raise RCDParseError(f"Failed to parse personal info: {e}") from e

    @staticmethod
    def _create_stats(data: Dict[str, str]) -> TalentStats:
        """
        Create TalentStats from parsed data.

        Args:
            data: Parsed key-value pairs

        Returns:
            TalentStats object

        Raises:
            RCDParseError: If required fields are missing or invalid
        """
        try:
            return TalentStats(
                aggression=float(data.get('Aggression', 50.0)),
                reputation=float(data.get('Reputation', 50.0)),
                courtesy=float(data.get('Courtesy', 50.0)),
                composure=float(data.get('Composure', 50.0)),
                speed=float(data.get('Speed', 50.0)),
                crash=float(data.get('Crash', 50.0)),
                recovery=float(data.get('Recovery', 50.0)),
                completed_laps=float(data.get('CompletedLaps', 90.0)),
                min_racing_skill=float(data.get('MinRacingSkill', 50.0)),
            )
        except (ValueError, KeyError) as e:
            raise RCDParseError(f"Failed to parse stats: {e}") from e
