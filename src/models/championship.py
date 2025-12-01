"""
Data models for rFactor Championship files (.cch).

A Championship represents a complete career season with all settings,
participants, and statistics.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CareerStats:
    """Career statistics for the player."""

    experience: int = 0
    money: int = 500
    cur_seas_index: int = 0
    single_player_vehicle: str = ""
    single_player_filter: str = ""
    multi_player_filter: str = ""
    ai_realism: float = 0.25
    single_player_ai_strength: int = 95
    multi_player_ai_strength: int = 95
    aborted_seasons: int = 0
    total_laps: int = 0
    total_races: int = 0
    total_races_with_ai: int = 0
    total_points_scored: int = 0
    total_championships: int = 0
    total_wins: int = 0
    total_poles: int = 0
    total_lap_records: int = 0
    avg_start_position: float = 0.0
    avg_finish_position: float = 0.0
    avg_race_distance: float = 0.0
    avg_opponent_strength: float = 0.0


@dataclass
class VehicleEntry:
    """Represents a vehicle owned by the player in career mode."""

    vehicle_id: int
    file: str
    skin: str = ""
    meters_driven: int = 0
    money_spent: int = 0
    free_vehicle: int = 1
    seat: tuple = (10.0, 10.0)
    mirror: tuple = (10.0, 10.0)
    upgrade_list: str = ""


@dataclass
class SeasonSettings:
    """Season configuration settings."""

    name: str = "New Season"
    season_status: int = 0  # 0=not started, 1=unknown/unused, 2=in progress (based on real .cch analysis)
    race_session: int = 0
    race_over: int = 0
    current_race: int = 0
    player_vehicle_id: int = 0

    # Mechanical settings
    mechfail_rate: int = 2
    gameopt_damagemultiplier: int = 50
    gameopt_fuel_mult: int = 1
    gameopt_tire_mult: int = 1

    # Race conditions
    racecond_reconnaissance: int = 0
    racecond_walkthrough: int = 1
    racecond_formation: int = 3
    racecond_safetycarcollision: int = 1
    racecond_safetycar_thresh: float = 1.0
    racecond_flag_rules: int = 2
    racecond_blue_flags: int = 7

    # Weather and time
    racecond_weather: int = 0
    racecond_timescaled_weather: int = 1
    racecond_race_starting_time: int = 840  # Minutes since midnight
    racecond_race_timescale: int = 1

    # Qualification and parc ferme
    racecond_private_qual: int = 2
    racecond_parc_ferme: int = 3

    # Game options
    gameopt_ai_driverstrength: int = 95
    gameopt_free_settings: int = -1
    gameopt_race_finish_criteria: int = 1  # 0=time, 1=laps
    gameopt_race_laps: int = 5
    gameopt_race_time: int = 120
    gameopt_race_length: float = 0.1
    gameopt_opponents: int = 9
    gameopt_speed_comp: int = 0
    gameopt_crash_recovery: int = 3


@dataclass
class Participant:
    """Base class for player and opponents."""

    name: str
    veh_file: str
    rcd_file: str = ""
    season_points: int = 0
    points_position: int = 0
    poles_taken: int = 0
    original_grid_position: int = 0
    current_grid_position: int = 0
    control_type: int = 1  # 0=player, 1=AI
    active: int = 1


@dataclass
class Player(Participant):
    """Player configuration in the championship."""

    control_type: int = 0  # Player is always control_type=0


@dataclass
class Opponent(Participant):
    """Opponent configuration in the championship."""

    opponent_id: int = 0  # For indexing (OPPONENT00, OPPONENT01, etc.)
    control_type: int = 1  # Opponents are AI by default


@dataclass
class TrackStat:
    """Statistics for a specific track."""

    track_name: str
    track_file: str
    class_records: List[tuple] = field(default_factory=list)  # List of (class, data...)


@dataclass
class Championship:
    """
    Represents a complete rFactor championship (.cch file).

    This is the main model that contains all championship data including
    career stats, vehicles, season settings, participants, and track stats.
    """

    # Main sections
    career: CareerStats = field(default_factory=CareerStats)
    vehicles: List[VehicleEntry] = field(default_factory=list)
    season: SeasonSettings = field(default_factory=SeasonSettings)
    player: Optional[Player] = None
    opponents: List[Opponent] = field(default_factory=list)
    track_stats: List[TrackStat] = field(default_factory=list)

    # Metadata
    file_path: Optional[str] = None

    def __post_init__(self):
        """Validate championship data."""
        if self.player is None:
            # Create default player if not provided
            self.player = Player(
                name="Player",
                veh_file="",
            )

    def get_opponent_by_id(self, opponent_id: int) -> Optional[Opponent]:
        """
        Get opponent by ID.

        Args:
            opponent_id: ID of the opponent (0-based)

        Returns:
            Opponent or None if not found
        """
        for opp in self.opponents:
            if opp.opponent_id == opponent_id:
                return opp
        return None

    def get_opponent_by_name(self, name: str) -> Optional[Opponent]:
        """
        Get opponent by name.

        Args:
            name: Name of the opponent

        Returns:
            Opponent or None if not found
        """
        for opp in self.opponents:
            if opp.name == name:
                return opp
        return None

    def add_opponent(self, opponent: Opponent) -> None:
        """
        Add an opponent to the championship.

        Args:
            opponent: Opponent to add
        """
        # Auto-assign ID if not set
        if opponent.opponent_id == 0 and self.opponents:
            max_id = max(opp.opponent_id for opp in self.opponents)
            opponent.opponent_id = max_id + 1

        self.opponents.append(opponent)

    def remove_opponent(self, opponent_id: int) -> bool:
        """
        Remove an opponent from the championship.

        Args:
            opponent_id: ID of the opponent to remove

        Returns:
            True if removed, False if not found
        """
        for i, opp in enumerate(self.opponents):
            if opp.opponent_id == opponent_id:
                self.opponents.pop(i)
                return True
        return False

    def get_participant_count(self) -> int:
        """
        Get total number of participants (player + opponents).

        Returns:
            Total participant count
        """
        return 1 + len(self.opponents)  # 1 player + N opponents

    def get_active_opponent_count(self) -> int:
        """
        Get number of active opponents.

        Returns:
            Number of active opponents
        """
        return sum(1 for opp in self.opponents if opp.active == 1)

    def to_dict(self) -> dict:
        """
        Convert championship to dictionary representation.

        Returns:
            Dictionary with all championship data
        """
        return {
            "career": self.career.__dict__,
            "vehicles": [v.__dict__ for v in self.vehicles],
            "season": self.season.__dict__,
            "player": self.player.__dict__ if self.player else None,
            "opponents": [o.__dict__ for o in self.opponents],
            "track_stats": [
                {
                    "track_name": ts.track_name,
                    "track_file": ts.track_file,
                    "class_records": ts.class_records,
                }
                for ts in self.track_stats
            ],
            "file_path": self.file_path,
        }

    def __str__(self) -> str:
        """String representation of the championship."""
        return (
            f"Championship(name='{self.season.name}', "
            f"player='{self.player.name if self.player else 'None'}', "
            f"opponents={len(self.opponents)}, "
            f"status={self.season.season_status})"
        )

    def __repr__(self) -> str:
        """Developer representation of the championship."""
        return (
            f"Championship(season={self.season.name!r}, "
            f"participants={self.get_participant_count()}, "
            f"vehicles={len(self.vehicles)})"
        )
