"""
Generator for rFactor Championship files (.cch).

Creates .cch files from Championship objects.
"""

from ..models.championship import Championship
from ..utils.file_utils import write_rfactor_file


class CCHGenerator:
    """Generator for .cch (Championship) files."""

    @staticmethod
    def generate(championship: Championship, filepath: str) -> None:
        """
        Generate a .cch file from a Championship object.

        Args:
            championship: Championship object to generate file for
            filepath: Path where to save the .cch file

        Raises:
            PermissionError: If file can't be written
        """
        content = CCHGenerator.to_content(championship)
        write_rfactor_file(filepath, content)

    @staticmethod
    def to_content(championship: Championship) -> str:
        """
        Convert a Championship object to .cch file content.

        Args:
            championship: Championship object to convert

        Returns:
            File content as string
        """
        lines = []

        # Header
        lines.append("//[[gMa1.002f (c)2007    ]] [[            ]]")

        # [CAREER] section
        lines.extend(CCHGenerator._generate_career(championship.career))

        # [VEHICLE] sections (multiple)
        for vehicle in championship.vehicles:
            lines.extend(CCHGenerator._generate_vehicle(vehicle))

        # [CAREERSEASON] section
        lines.extend(CCHGenerator._generate_season(championship.season))

        # [PLAYER] section
        if championship.player:
            lines.extend(CCHGenerator._generate_player(championship.player))

        # [OPPONENTxx] sections (multiple)
        for opponent in championship.opponents:
            lines.extend(CCHGenerator._generate_opponent(opponent))

        # [PLAYERTRACKSTAT] sections (multiple)
        for track_stat in championship.track_stats:
            lines.extend(CCHGenerator._generate_track_stat(track_stat))

        # Empty line at end
        lines.append("")

        return '\n'.join(lines)

    @staticmethod
    def _generate_career(career) -> list:
        """Generate [CAREER] section."""
        lines = ["[CAREER]"]
        lines.append(f"Experience={career.experience}")
        lines.append(f"Money={career.money}")
        lines.append(f"CurSeasIndex={career.cur_seas_index}")
        lines.append(f'SinglePlayerVehicle="{career.single_player_vehicle}"')
        lines.append(f'SinglePlayerFilter="{career.single_player_filter}"')
        lines.append(f'MultiPlayerFilter="{career.multi_player_filter}"')
        lines.append(f"AIRealism={career.ai_realism:.4f}")
        lines.append(f"SinglePlayerAIStrength={career.single_player_ai_strength}")
        lines.append(f"MultiPlayerAIStrength={career.multi_player_ai_strength}")
        lines.append(f"AbortedSeasons={career.aborted_seasons}")
        lines.append(f"TotalLaps={career.total_laps}")
        lines.append(f"TotalRaces={career.total_races}")
        lines.append(f"TotalRacesWithAI={career.total_races_with_ai}")
        lines.append(f"TotalPointsScored={career.total_points_scored}")
        lines.append(f"TotalChampionships={career.total_championships}")
        lines.append(f"TotalWins={career.total_wins}")
        lines.append(f"TotalPoles={career.total_poles}")
        lines.append(f"TotalLapRecords={career.total_lap_records}")
        lines.append(f"AvgStartPosition={career.avg_start_position:.6f}")
        lines.append(f"AvgFinishPosition={career.avg_finish_position:.6f}")
        lines.append(f"AvgRaceDistance={career.avg_race_distance:.6f}")
        lines.append(f"AvgOpponentStrength={career.avg_opponent_strength:.6f}")
        return lines

    @staticmethod
    def _generate_vehicle(vehicle) -> list:
        """Generate [VEHICLE] section."""
        lines = ["[VEHICLE]"]
        lines.append(f"ID={vehicle.vehicle_id}")
        lines.append(f'File="{vehicle.file}"')
        lines.append(f'Skin="{vehicle.skin}"')
        lines.append(f"MetersDriven={vehicle.meters_driven}")
        lines.append(f"MoneySpent={vehicle.money_spent}")
        lines.append(f"FreeVehicle={vehicle.free_vehicle}")
        lines.append(f"Seat=({vehicle.seat[0]:.3f},{vehicle.seat[1]:.3f})")
        lines.append(f"Mirror=({vehicle.mirror[0]:.3f},{vehicle.mirror[1]:.3f})")
        lines.append(f"UpgradeList:{vehicle.upgrade_list}")
        lines.append("")  # Empty line after each vehicle
        return lines

    @staticmethod
    def _generate_season(season) -> list:
        """Generate [CAREERSEASON] section."""
        lines = ["[CAREERSEASON]"]
        lines.append(f'Name="{season.name}"')
        lines.append(f"SeasonStatus={season.season_status}")
        lines.append(f"RaceSession={season.race_session}")
        lines.append(f"RaceOver={season.race_over}")
        lines.append(f"CurrentRace={season.current_race}")
        lines.append(f"PlayerVehicleID={season.player_vehicle_id}")

        # Comment
        lines.append("// Season championship settings (these override the plr file values)")

        # Mechanical settings
        lines.append(f"MECHFAIL_rate={season.mechfail_rate}")

        # Race conditions
        lines.append(f"RACECOND_reconnaissance={season.racecond_reconnaissance}")
        lines.append(f"RACECOND_walkthrough={season.racecond_walkthrough}")
        lines.append(f"RACECOND_formation={season.racecond_formation}")
        lines.append(f"RACECOND_safetycarcollision={season.racecond_safetycarcollision}")
        lines.append(f"RACECOND_safetycar_thresh={season.racecond_safetycar_thresh:.6f}")
        lines.append(f"RACECOND_flag_rules={season.racecond_flag_rules}")
        lines.append(f"RACECOND_blue_flags={season.racecond_blue_flags}")
        lines.append(f"RACECOND_weather={season.racecond_weather}")
        lines.append(f"RACECOND_timescaled_weather={season.racecond_timescaled_weather}")
        lines.append(f"RACECOND_race_starting_time={season.racecond_race_starting_time}")
        lines.append(f"RACECOND_race_timescale={season.racecond_race_timescale}")
        lines.append(f"RACECOND_private_qual={season.racecond_private_qual}")
        lines.append(f"RACECOND_parc_ferme={season.racecond_parc_ferme}")

        # Game options
        lines.append(f"GAMEOPT_ai_driverstrength={season.gameopt_ai_driverstrength}")
        lines.append(f"GAMEOPT_free_settings={season.gameopt_free_settings}")
        lines.append(f"GAMEOPT_damagemultiplier={season.gameopt_damagemultiplier}")
        lines.append(f"GAMEOPT_race_finish_criteria={season.gameopt_race_finish_criteria}")
        lines.append(f"GAMEOPT_race_laps={season.gameopt_race_laps}")
        lines.append(f"GAMEOPT_race_time={season.gameopt_race_time}")
        lines.append(f"GAMEOPT_race_length={season.gameopt_race_length:.6f}")
        lines.append(f"GAMEOPT_opponents={season.gameopt_opponents}")
        lines.append(f"GAMEOPT_fuel_mult={season.gameopt_fuel_mult}")
        lines.append(f"GAMEOPT_tire_mult={season.gameopt_tire_mult}")
        lines.append(f"GAMEOPT_speed_comp={season.gameopt_speed_comp}")
        lines.append(f"GAMEOPT_crash_recovery={season.gameopt_crash_recovery}")

        return lines

    @staticmethod
    def _generate_player(player) -> list:
        """Generate [PLAYER] section."""
        lines = ["[PLAYER]"]
        lines.append(f'Name="{player.name}"')
        lines.append(f'VehFile="{player.veh_file}"')
        lines.append(f'RCDFile="{player.rcd_file}"')
        lines.append(f"SeasonPoints={player.season_points}")
        lines.append(f"PointsPosition={player.points_position}")
        lines.append(f"PolesTaken={player.poles_taken}")
        lines.append(f"OriginalGridPosition={player.original_grid_position}")
        lines.append(f"CurrentGridPosition={player.current_grid_position}")
        lines.append(f"ControlType={player.control_type}")
        lines.append(f"Active={player.active}")
        lines.append("")  # Empty line after player
        return lines

    @staticmethod
    def _generate_opponent(opponent) -> list:
        """Generate [OPPONENTxx] section."""
        # Format opponent ID with leading zeros (00, 01, 02, ...)
        section_name = f"OPPONENT{opponent.opponent_id:02d}"

        lines = [f"[{section_name}]"]
        lines.append(f'Name="{opponent.name}"')
        lines.append(f'VehFile="{opponent.veh_file}"')
        lines.append(f'RCDFile="{opponent.rcd_file}"')
        lines.append(f"SeasonPoints={opponent.season_points}")
        lines.append(f"PointsPosition={opponent.points_position}")
        lines.append(f"PolesTaken={opponent.poles_taken}")
        lines.append(f"OriginalGridPosition={opponent.original_grid_position}")
        lines.append(f"CurrentGridPosition={opponent.current_grid_position}")
        lines.append(f"ControlType={opponent.control_type}")
        lines.append(f"Active={opponent.active}")
        lines.append("")  # Empty line after opponent
        return lines

    @staticmethod
    def _generate_track_stat(track_stat) -> list:
        """Generate [PLAYERTRACKSTAT] section."""
        lines = ["[PLAYERTRACKSTAT]"]
        lines.append(f"TrackName={track_stat.track_name}")
        lines.append(f"TrackFile={track_stat.track_file}")

        # Generate ClassRecord entries
        for record in track_stat.class_records:
            lines.append(f"ClassRecord={record}")

        lines.append("")  # Empty line after track stat
        return lines
