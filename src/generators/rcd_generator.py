"""
Generator for rFactor Talent files (.rcd).

Creates .rcd files from Talent objects.
"""

from ..models.talent import Talent
from ..utils.file_utils import write_rfactor_file


class RCDGenerator:
    """Generator for .rcd (Talent) files."""

    @staticmethod
    def generate(talent: Talent, filepath: str) -> None:
        """
        Generate a .rcd file from a Talent object.

        Args:
            talent: Talent object to generate file for
            filepath: Path where to save the .rcd file

        Raises:
            PermissionError: If file can't be written
        """
        content = RCDGenerator.to_content(talent)
        write_rfactor_file(filepath, content)

    @staticmethod
    def to_content(talent: Talent) -> str:
        """
        Convert a Talent object to .rcd file content.

        Args:
            talent: Talent object to convert

        Returns:
            File content as string
        """
        lines = []

        # Name (first line)
        lines.append(talent.name)

        # Opening brace
        lines.append('{')

        # Driver Info section
        lines.append('//Driver Info')
        info = talent.personal_info
        lines.append(f'  Nationality={info.nationality}')
        lines.append(f'  DateofBirth={info.date_of_birth}')
        lines.append(f'  Starts={info.starts}')
        lines.append(f'  Poles={info.poles}')
        lines.append(f'  Wins={info.wins}')
        lines.append(f'  DriversChampionships={info.drivers_championships}')

        # Empty line between sections
        lines.append('')

        # Driver Stats section
        lines.append('//Driver Stats')
        stats = talent.stats
        lines.append(f'  Aggression={stats.aggression:.2f}')
        lines.append(f'  Reputation={stats.reputation:.2f}')
        lines.append(f'  Courtesy={stats.courtesy:.2f}')
        lines.append(f'  Composure={stats.composure:.2f}')
        lines.append(f'  Speed={stats.speed:.2f}')
        lines.append(f'  Crash={stats.crash:.2f}')
        lines.append(f'  Recovery={stats.recovery:.2f}')
        lines.append(f'  CompletedLaps={stats.completed_laps:.2f}')
        lines.append(f'  MinRacingSkill={stats.min_racing_skill:.2f}')

        # Closing brace
        lines.append('}')

        # Empty line at end
        lines.append('')

        return '\n'.join(lines)
