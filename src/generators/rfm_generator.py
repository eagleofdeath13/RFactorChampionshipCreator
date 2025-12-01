"""
Generator for rFactor RFM (RFactor Mod) files.

Creates RFM files from RFMod objects.
"""

from pathlib import Path
from typing import TextIO

from ..models.rfm import RFMod


class RFMGenerator:
    """Generator for RFM files."""

    def __init__(self, rfm: RFMod):
        """
        Initialize generator.

        Args:
            rfm: RFMod object to generate
        """
        self.rfm = rfm

    def generate(self, output_path: str) -> None:
        """
        Generate RFM file.

        Args:
            output_path: Path where to write the RFM file

        Example:
            >>> rfm = RFMod(mod_name="My Championship", vehicle_filter="RFTOOL_MyChamp")
            >>> generator = RFMGenerator(rfm)
            >>> generator.generate("my_championship.rfm")
        """
        output_file = Path(output_path)

        # Create parent directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write file with proper encoding
        with open(output_file, 'w', encoding='windows-1252') as f:
            self._write_header(f)
            self._write_config_overrides(f)
            self._write_seasons(f)
            self._write_default_scoring(f)
            self._write_career_settings(f)
            self._write_season_scoring_info(f)
            self._write_scene_order(f)
            self._write_pit_group_order(f)

    def _write_header(self, f: TextIO) -> None:
        """Write file header and main configuration."""
        f.write("// Game/Season Info:\n")
        f.write(f"Mod Name = {self.rfm.mod_name}\n")
        f.write(f"Track Filter = {self.rfm.track_filter}\n")
        f.write(f"Vehicle Filter = {self.rfm.vehicle_filter}\n")
        f.write(f"SafetyCar = {self.rfm.safety_car}\n")
        f.write("\n")

        # Network settings
        f.write(f"Matchmaker = {self.rfm.matchmaker}\n")
        f.write(f"Matchmaker TCP Port = {self.rfm.matchmaker_tcp_port}\n")
        f.write(f"Matchmaker UDP Port = {self.rfm.matchmaker_udp_port}\n")
        f.write(f"Loading Bar Color = {self.rfm.loading_bar_color}\n")
        f.write(f"RaceCast Location = {self.rfm.racecast_location}\n")
        f.write("\n")

        # Opponents
        f.write(f"Max Opponents = {self.rfm.max_opponents}   // maximum opponents in practice/quick race/grand prix/championship\n")
        f.write(f"Min Championship Opponents = {self.rfm.min_championship_opponents} // minimum opponents in championship only\n")
        f.write("\n")

    def _write_config_overrides(self, f: TextIO) -> None:
        """Write ConfigOverrides section (if any)."""
        if not self.rfm.config_overrides:
            return

        f.write("ConfigOverrides\n")
        f.write("{\n")

        for key, value in self.rfm.config_overrides.items():
            f.write(f"  {key}={value}\n")

        f.write("}\n\n")

    def _write_seasons(self, f: TextIO) -> None:
        """Write all seasons."""
        if not self.rfm.seasons:
            return

        f.write("// Seasons:\n\n")

        for season in self.rfm.seasons:
            f.write(f"Season = {season.name}\n")
            f.write("{\n")

            # Season parameters
            f.write(f"  Vehicle Filter = {season.vehicle_filter}\n")
            f.write(f"  Min Championship Opponents = {season.min_championship_opponents}\n")

            if season.full_season_name:
                f.write(f"  FullSeasonName = {season.full_season_name}\n")

            if season.min_experience is not None:
                f.write(f"  MinExperience = {season.min_experience}\n")

            if season.entry_fee is not None:
                f.write(f"  EntryFee = {season.entry_fee}\n")

            # Scene order
            if season.scene_order:
                f.write("\n  SceneOrder\n")
                f.write("  {\n")
                for track in season.scene_order:
                    f.write(f"    {track}\n")
                f.write("  }\n")

            f.write("}\n\n")

    def _write_default_scoring(self, f: TextIO) -> None:
        """Write DefaultScoring section."""
        s = self.rfm.default_scoring

        f.write("\nDefaultScoring\n")
        f.write("{\n")

        # Pit speeds
        f.write(f"  RacePitKPH = {s.race_pit_kph}\n")
        f.write(f"  NormalPitKPH = {s.normal_pit_kph}\n")

        # Practice sessions
        f.write(f"  Practice1Day = {s.practice1_day}\n")
        f.write(f"  Practice1Start = {s.practice1_start}\n")
        f.write(f"  Practice1Duration = {s.practice1_duration}\n")

        f.write(f"  Practice2Day = {s.practice2_day}\n")
        f.write(f"  Practice2Start = {s.practice2_start}\n")
        f.write(f"  Practice2Duration = {s.practice2_duration}\n")

        f.write(f"  Practice3Day = {s.practice3_day}\n")
        f.write(f"  Practice3Start = {s.practice3_start}\n")
        f.write(f"  Practice3Duration = {s.practice3_duration}\n")

        f.write(f"  Practice4Day = {s.practice4_day}\n")
        f.write(f"  Practice4Start = {s.practice4_start}\n")
        f.write(f"  Practice4Duration = {s.practice4_duration}\n")

        # Qualifying
        f.write(f"  QualifyDay = {s.qualify_day}\n")
        f.write(f"  QualifyStart = {s.qualify_start}\n")
        f.write(f"  QualifyDuration = {s.qualify_duration}\n")
        f.write(f"  QualifyLaps = {s.qualify_laps}\n")

        # Warmup
        f.write(f"  WarmupDay = {s.warmup_day}\n")
        f.write(f"  WarmupStart = {s.warmup_start}\n")
        f.write(f"  WarmupDuration = {s.warmup_duration}\n")

        # Race
        f.write(f"  RaceDay = {s.race_day}\n")
        f.write(f"  RaceStart = {s.race_start}\n")
        f.write(f"  RaceLaps = {s.race_laps}\n")
        f.write(f"  RaceTime = {s.race_time}\n")

        f.write("}\n\n")

    def _write_career_settings(self, f: TextIO) -> None:
        """Write career mode settings."""
        c = self.rfm.career_settings

        f.write("// Money and experience accumulation (mostly multipliers for hard-coded values\n")
        f.write("// which have various factors taken into account like number of competitors)\n")

        f.write(f"StartingMoney = {c.starting_money}          // you might need a little spendin' cash\n")
        f.write(f"StartingExperience = {c.starting_experience}       // start with no experience\n")

        # Starting vehicles
        for vehicle in c.starting_vehicles:
            f.write(f"StartingVehicle = {vehicle}         // randomly chooses one free vehicle from this list\n")

        f.write(f"DriveAnyUnlocked = {c.drive_any_unlocked}         // 0 = must own to drive, 1 = must be unlocked to drive, 2 = drive anything\n")

        # Multipliers
        f.write(f"BaseCreditMult = {c.base_credit_mult}         // base which is multiplied by all the other multipliers\n")
        f.write(f"LapMoneyMult = {c.lap_money_mult}           // laps completed (based roughly on expected lap times)\n")
        f.write(f"LapExpMult = {c.lap_exp_mult}\n")
        f.write(f"FineMoneyMult = {c.fine_money_mult}          // fines\n")
        f.write(f"FineExpMult = {c.fine_exp_mult}\n")

        f.write(f"PoleSingleMoneyMult = {c.pole_single_money_mult}    // pole positions in single player\n")
        f.write(f"PoleSingleExpMult = {c.pole_single_exp_mult}\n")
        f.write(f"PoleCareerMoneyMult = {c.pole_career_money_mult}    // pole positions in career mode\n")
        f.write(f"PoleCareerExpMult = {c.pole_career_exp_mult}\n")
        f.write(f"PoleMultiMoneyMult = {c.pole_multi_money_mult}     // pole positions in multiplayer\n")
        f.write(f"PoleMultiExpMult = {c.pole_multi_exp_mult}\n")

        f.write(f"WinSingleMoneyMult = {c.win_single_money_mult}     // wins in single player\n")
        f.write(f"WinSingleExpMult = {c.win_single_exp_mult}\n")
        f.write(f"WinCareerMoneyMult = {c.win_career_money_mult}     // wins in career mode\n")
        f.write(f"WinCareerExpMult = {c.win_career_exp_mult}\n")
        f.write(f"WinMultiMoneyMult = {c.win_multi_money_mult}      // wins in multiplayer\n")
        f.write(f"WinMultiExpMult = {c.win_multi_exp_mult}\n")

        f.write(f"PointsSingleMoneyMult = {c.points_single_money_mult}  // points in single player\n")
        f.write(f"PointsSingleExpMult = {c.points_single_exp_mult}\n")
        f.write(f"PointsCareerMoneyMult = {c.points_career_money_mult}  // points in career mode\n")
        f.write(f"PointsCareerExpMult = {c.points_career_exp_mult}\n")
        f.write(f"PointsMultiMoneyMult = {c.points_multi_money_mult}   // points in multiplayer\n")
        f.write(f"PointsMultiExpMult = {c.points_multi_exp_mult}\n")

        f.write("\n")

    def _write_season_scoring_info(self, f: TextIO) -> None:
        """Write season scoring points distribution."""
        s = self.rfm.season_scoring_info

        f.write("// Season scoring info\n")
        f.write("SeasonScoringInfo\n")
        f.write("{\n")

        f.write(f"  FirstPlace = {s.first_place}\n")
        f.write(f"  SecondPlace = {s.second_place}\n")
        f.write(f"  ThirdPlace = {s.third_place}\n")
        f.write(f"  FourthPlace = {s.fourth_place}\n")
        f.write(f"  FifthPlace = {s.fifth_place}\n")
        f.write(f"  SixthPlace = {s.sixth_place}\n")
        f.write(f"  SeventhPlace = {s.seventh_place}\n")
        f.write(f"  EighthPlace = {s.eighth_place}\n")

        f.write("}\n\n")

    def _write_scene_order(self, f: TextIO) -> None:
        """Write global scene order."""
        if not self.rfm.scene_order:
            return

        f.write("SceneOrder\n")
        f.write("{\n")

        for track in self.rfm.scene_order:
            f.write(f"  {track}\n")

        f.write("}\n\n")

    def _write_pit_group_order(self, f: TextIO) -> None:
        """Write pit group configuration."""
        if not self.rfm.pit_group_order:
            return

        f.write("// Pitstop locations in order from front to back, with the number\n")
        f.write("// of vehicles sharing each pit ... if the order needs to be\n")
        f.write("// reversed on an individual track, set \"ReversePitOrder=1\" in\n")
        f.write("// the track-specific GDB file.\n")
        f.write("// These are now \"pit group\" names, not necessarily team names.\n")
        f.write("// In the VEH file, the pit group defaults to the team name but\n")
        f.write("// can be overridden by defining \"PitGroup=<name>\".\n")
        f.write(f"PitOrderByQualifying = {'true' if self.rfm.pit_order_by_qualifying else 'false'}    // whether to set the pit order in the race by qualifying results\n")
        f.write("PitGroupOrder\n")
        f.write("{\n")

        f.write("  // format is: PitGroup = <# of vehicles sharing pit>, <groupname>\n")
        for pit_group in self.rfm.pit_group_order:
            f.write(f"  PitGroup = {pit_group.num_vehicles}, {pit_group.group_name}\n")

        f.write("}\n\n")


def generate_rfm(rfm: RFMod, output_path: str) -> None:
    """
    Generate an RFM file from an RFMod object.

    Args:
        rfm: RFMod object
        output_path: Path where to write the file

    Example:
        >>> from src.models.rfm import RFMod, Season
        >>> rfm = RFMod(
        ...     mod_name="My Championship",
        ...     vehicle_filter="RFTOOL_MyChamp"
        ... )
        >>> rfm.add_season(Season(
        ...     name="Season 1",
        ...     vehicle_filter="RFTOOL_MyChamp",
        ...     scene_order=["Mills_Short", "Toban_Long"]
        ... ))
        >>> generate_rfm(rfm, "my_championship.rfm")
    """
    generator = RFMGenerator(rfm)
    generator.generate(output_path)
