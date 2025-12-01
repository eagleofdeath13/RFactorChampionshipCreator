"""
Data models for rFactor Talent (driver) files (.rcd).

A Talent represents a driver with personal information and racing statistics.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TalentPersonalInfo:
    """Personal information about a driver."""

    nationality: str
    date_of_birth: str  # Format: DD-MM-YYYY
    starts: int = 0
    poles: int = 0
    wins: int = 0
    drivers_championships: int = 0

    def __post_init__(self):
        """Validate personal info data."""
        if self.starts < 0:
            raise ValueError("Starts must be >= 0")
        if self.poles < 0:
            raise ValueError("Poles must be >= 0")
        if self.wins < 0:
            raise ValueError("Wins must be >= 0")
        if self.drivers_championships < 0:
            raise ValueError("Drivers championships must be >= 0")


@dataclass
class TalentStats:
    """Racing statistics for a driver.

    All stats are float values between 0.0 and 100.0.
    Higher values are better except for 'crash' (lower is better).
    """

    aggression: float = 50.0        # Driver aggression in racing
    reputation: float = 50.0        # Driver reputation
    courtesy: float = 50.0          # Fair play / courtesy
    composure: float = 50.0         # Ability to stay calm under pressure
    speed: float = 50.0             # Pure speed ability
    crash: float = 50.0             # Crash tendency (lower is better)
    recovery: float = 50.0          # Ability to recover from mistakes
    completed_laps: float = 90.0    # Percentage of laps completed
    min_racing_skill: float = 50.0  # Minimum racing skill level

    def __post_init__(self):
        """Validate that all stats are in valid range [0, 100]."""
        stats = {
            'aggression': self.aggression,
            'reputation': self.reputation,
            'courtesy': self.courtesy,
            'composure': self.composure,
            'speed': self.speed,
            'crash': self.crash,
            'recovery': self.recovery,
            'completed_laps': self.completed_laps,
            'min_racing_skill': self.min_racing_skill,
        }

        for stat_name, value in stats.items():
            if not 0.0 <= value <= 100.0:
                raise ValueError(
                    f"{stat_name} must be between 0.0 and 100.0, got {value}"
                )


@dataclass
class Talent:
    """
    Represents a rFactor driver (Talent).

    A Talent file (.rcd) contains driver information and statistics.
    """

    name: str
    personal_info: TalentPersonalInfo
    stats: TalentStats
    file_path: Optional[str] = None  # Path to the .rcd file

    def __post_init__(self):
        """Validate talent data."""
        if not self.name or not self.name.strip():
            raise ValueError("Talent name cannot be empty")

    @property
    def filename(self) -> str:
        """
        Get the expected filename for this talent.

        Returns:
            Filename without spaces (e.g., "BrandonLang.rcd")

        Example:
            >>> talent = Talent(name="Brandon Lang", ...)
            >>> talent.filename
            'BrandonLang.rcd'
        """
        normalized_name = self.name.replace(' ', '')
        return f"{normalized_name}.rcd"

    def to_dict(self) -> dict:
        """
        Convert talent to dictionary representation.

        Returns:
            Dictionary with all talent data
        """
        return {
            'name': self.name,
            'personal_info': {
                'nationality': self.personal_info.nationality,
                'date_of_birth': self.personal_info.date_of_birth,
                'starts': self.personal_info.starts,
                'poles': self.personal_info.poles,
                'wins': self.personal_info.wins,
                'drivers_championships': self.personal_info.drivers_championships,
            },
            'stats': {
                'aggression': self.stats.aggression,
                'reputation': self.stats.reputation,
                'courtesy': self.stats.courtesy,
                'composure': self.stats.composure,
                'speed': self.stats.speed,
                'crash': self.stats.crash,
                'recovery': self.stats.recovery,
                'completed_laps': self.stats.completed_laps,
                'min_racing_skill': self.stats.min_racing_skill,
            },
            'file_path': self.file_path,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Talent':
        """
        Create a Talent from dictionary representation.

        Args:
            data: Dictionary with talent data

        Returns:
            Talent instance
        """
        personal_info = TalentPersonalInfo(**data['personal_info'])
        stats = TalentStats(**data['stats'])

        return cls(
            name=data['name'],
            personal_info=personal_info,
            stats=stats,
            file_path=data.get('file_path'),
        )

    def __str__(self) -> str:
        """String representation of the talent."""
        return (
            f"Talent(name='{self.name}', "
            f"nationality='{self.personal_info.nationality}', "
            f"speed={self.stats.speed:.2f})"
        )

    def __repr__(self) -> str:
        """Developer representation of the talent."""
        return (
            f"Talent(name='{self.name}', "
            f"personal_info={self.personal_info!r}, "
            f"stats={self.stats!r})"
        )
