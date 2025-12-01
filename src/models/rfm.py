"""
Data models for rFactor RFM (RFactor Mod) files.

RFM files define championships/seasons with their rules, circuits, scoring, etc.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Season:
    """Represents a season within an RFM championship."""
    name: str
    vehicle_filter: str
    scene_order: List[str]  # List of track names
    min_championship_opponents: int = 5
    full_season_name: Optional[str] = None
    min_experience: Optional[int] = None
    entry_fee: Optional[int] = None


@dataclass
class DefaultScoring:
    """Default scoring and session configuration."""
    # Pit speed limits
    race_pit_kph: int = 80
    normal_pit_kph: int = 80

    # Practice sessions
    practice1_day: str = "Friday"
    practice1_start: str = "10:00"
    practice1_duration: int = 60
    practice2_day: str = "Friday"
    practice2_start: str = "13:00"
    practice2_duration: int = 60
    practice3_day: str = "Saturday"
    practice3_start: str = "9:00"
    practice3_duration: int = 45
    practice4_day: str = "Saturday"
    practice4_start: str = "10:15"
    practice4_duration: int = 45

    # Qualifying
    qualify_day: str = "Saturday"
    qualify_start: str = "14:00"
    qualify_duration: int = 60
    qualify_laps: int = 12

    # Warmup
    warmup_day: str = "Sunday"
    warmup_start: str = "9:00"
    warmup_duration: int = 30

    # Race
    race_day: str = "Sunday"
    race_start: str = "12:00"
    race_laps: int = 50
    race_time: int = 120


@dataclass
class SeasonScoringInfo:
    """Points distribution for season standings."""
    first_place: int = 10
    second_place: int = 8
    third_place: int = 6
    fourth_place: int = 5
    fifth_place: int = 4
    sixth_place: int = 3
    seventh_place: int = 2
    eighth_place: int = 1


@dataclass
class PitGroup:
    """Pit group configuration."""
    num_vehicles: int
    group_name: str


@dataclass
class CareerSettings:
    """Career mode settings (money, experience, multipliers)."""
    # Starting values
    starting_money: int = 500000000  # Plenty of cash to buy vehicles
    starting_experience: int = 0
    starting_vehicles: List[str] = field(default_factory=list)
    drive_any_unlocked: int = 0

    # Credit multipliers
    base_credit_mult: float = 1.0
    lap_money_mult: float = 1.0
    lap_exp_mult: float = 1.0
    fine_money_mult: float = 1.0
    fine_exp_mult: float = 0.0

    # Pole position multipliers
    pole_single_money_mult: float = 1.0
    pole_single_exp_mult: float = 1.0
    pole_career_money_mult: float = 1.0
    pole_career_exp_mult: float = 1.0
    pole_multi_money_mult: float = 1.0
    pole_multi_exp_mult: float = 1.0

    # Win multipliers
    win_single_money_mult: float = 1.0
    win_single_exp_mult: float = 1.0
    win_career_money_mult: float = 1.0
    win_career_exp_mult: float = 1.0
    win_multi_money_mult: float = 1.0
    win_multi_exp_mult: float = 1.0

    # Points multipliers
    points_single_money_mult: float = 1.0
    points_single_exp_mult: float = 1.0
    points_career_money_mult: float = 1.0
    points_career_exp_mult: float = 1.0
    points_multi_money_mult: float = 1.0
    points_multi_exp_mult: float = 1.0


@dataclass
class RFMod:
    """
    Represents an rFactor Mod (RFM file).

    This defines a championship with its seasons, rules, scoring, etc.
    """
    # Basic info
    mod_name: str
    vehicle_filter: str
    track_filter: str = "*"
    safety_car: str = "Hammer_PC.veh"

    # Opponents
    max_opponents: int = 19
    min_championship_opponents: int = 3

    # Seasons
    seasons: List[Season] = field(default_factory=list)

    # Scoring
    default_scoring: DefaultScoring = field(default_factory=DefaultScoring)
    season_scoring_info: SeasonScoringInfo = field(default_factory=SeasonScoringInfo)

    # Career settings
    career_settings: CareerSettings = field(default_factory=CareerSettings)

    # Global scene order (default track list)
    scene_order: List[str] = field(default_factory=list)

    # Pit groups
    pit_order_by_qualifying: bool = False
    pit_group_order: List[PitGroup] = field(default_factory=list)

    # Network settings (optional)
    matchmaker: str = "match.rfactor.net"
    matchmaker_tcp_port: int = 39001
    matchmaker_udp_port: int = 39002
    racecast_location: str = "racecast.rfactor.net"
    loading_bar_color: int = 16750848

    # Config overrides (optional)
    config_overrides: Dict[str, str] = field(default_factory=dict)

    # File path (populated after loading)
    file_path: Optional[str] = None

    def __str__(self) -> str:
        """String representation."""
        season_count = len(self.seasons)
        return f"RFMod(mod_name='{self.mod_name}', seasons={season_count})"

    def get_season_by_name(self, name: str) -> Optional[Season]:
        """Get a season by its name."""
        for season in self.seasons:
            if season.name == name:
                return season
        return None

    def add_season(self, season: Season) -> None:
        """Add a season to the mod."""
        self.seasons.append(season)

    def get_total_tracks(self) -> int:
        """Get total number of unique tracks across all seasons."""
        all_tracks = set()
        for season in self.seasons:
            all_tracks.update(season.scene_order)
        return len(all_tracks)
