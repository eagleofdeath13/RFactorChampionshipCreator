"""API routes for championships management."""

from fastapi import APIRouter, HTTPException, status
from typing import List

from ..schemas.championship import (
    ChampionshipCreateSchema,
    ChampionshipInfoSchema,
    ChampionshipDetailSchema,
)
from ...services.championship_service import ChampionshipService
from ...utils.config import get_config

router = APIRouter()


def get_championship_service() -> ChampionshipService:
    """Get ChampionshipService instance."""
    config = get_config()
    if not config.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not configured. Please configure rFactor path first."
        )
    return ChampionshipService(
        config.get_rfactor_path(),
        config.get_current_player()
    )


@router.get("/", response_model=List[ChampionshipInfoSchema])
async def list_championships():
    """
    List all championships.

    Returns a list of all available championships with basic information.
    """
    service = get_championship_service()
    championships = service.list_all_with_info()

    return [
        ChampionshipInfoSchema(**info)
        for info in championships
    ]


@router.get("/rfm/{name}")
async def get_rfm_championship(name: str):
    """
    Get a specific RFM championship definition.

    Args:
        name: Name of the RFM file (without .rfm extension)

    Returns:
        Complete RFM championship definition

    Raises:
        404: RFM championship not found
    """
    service = get_championship_service()
    rfm = service.get_rfm(name)

    if not rfm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RFM Championship '{name}' not found"
        )

    # Check if this is a custom championship
    is_custom = name.startswith('M_')

    # Build RFM championship data
    return {
        "name": rfm.mod_name,
        "is_custom": is_custom,
        "is_rfm": True,
        "type": "RFM",
        "seasons": [
            {
                "name": season.name,
                "tracks": season.scene_order,
                "vehicle_filter": season.vehicle_filter,
                "min_opponents": season.min_championship_opponents,
            }
            for season in rfm.seasons
        ] if rfm.seasons else [],
    }


@router.get("/{name}")
async def get_championship(name: str):
    """
    Get a specific championship by name with complete data.

    Args:
        name: Name of the championship file (without .cch)

    Returns:
        Complete championship details including all settings, opponents, vehicles, tracks

    Raises:
        404: Championship not found
    """
    service = get_championship_service()
    championship = service.get(name)

    if not championship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Championship '{name}' not found"
        )

    # Build comprehensive championship data
    return {
        # Basic info
        "name": championship.season.name,
        "status": championship.season.season_status,
        "current_race": championship.season.current_race,

        # Game options
        "game_options": {
            "race_laps": championship.season.gameopt_race_laps,
            "race_time": championship.season.gameopt_race_time,
            "race_length": championship.season.gameopt_race_length,
            "race_finish_criteria": championship.season.gameopt_race_finish_criteria,
            "ai_strength": championship.season.gameopt_ai_driverstrength,
            "opponents": championship.season.gameopt_opponents,
            "damage_multiplier": championship.season.gameopt_damagemultiplier,
            "tire_mult": championship.season.gameopt_tire_mult,
            "fuel_mult": championship.season.gameopt_fuel_mult,
            "mechfail_rate": championship.season.mechfail_rate,
            "speed_comp": championship.season.gameopt_speed_comp,
            "crash_recovery": championship.season.gameopt_crash_recovery,
            "free_settings": championship.season.gameopt_free_settings,
        },

        # Race conditions
        "race_conditions": {
            "reconnaissance": championship.season.racecond_reconnaissance,
            "walkthrough": championship.season.racecond_walkthrough,
            "formation": championship.season.racecond_formation,
            "weather": championship.season.racecond_weather,
            "timescaled_weather": championship.season.racecond_timescaled_weather,
            "race_starting_time": championship.season.racecond_race_starting_time,
            "race_timescale": championship.season.racecond_race_timescale,
            "private_qual": championship.season.racecond_private_qual,
            "parc_ferme": championship.season.racecond_parc_ferme,
            "flag_rules": championship.season.racecond_flag_rules,
            "blue_flags": championship.season.racecond_blue_flags,
            "safetycar_collision": championship.season.racecond_safetycarcollision,
            "safetycar_thresh": championship.season.racecond_safetycar_thresh,
        },

        # Player info
        "player": {
            "name": championship.player.name,
            "veh_file": championship.player.veh_file,
            "rcd_file": championship.player.rcd_file,
            "season_points": championship.player.season_points,
            "points_position": championship.player.points_position,
            "poles_taken": championship.player.poles_taken,
            "original_grid_position": championship.player.original_grid_position,
            "current_grid_position": championship.player.current_grid_position,
        } if championship.player else None,

        # Opponents with full details
        "opponents": [
            {
                "opponent_id": opp.opponent_id,
                "name": opp.name,
                "veh_file": opp.veh_file,
                "rcd_file": opp.rcd_file,
                "season_points": opp.season_points,
                "points_position": opp.points_position,
                "poles_taken": opp.poles_taken,
                "original_grid_position": opp.original_grid_position,
                "current_grid_position": opp.current_grid_position,
            }
            for opp in championship.opponents
        ],

        # Vehicle entries
        "vehicle_entries": [
            {
                "vehicle_id": ve.vehicle_id,
                "file": ve.file,
                "skin": ve.skin,
                "meters_driven": ve.meters_driven,
                "money_spent": ve.money_spent,
                "free_vehicle": ve.free_vehicle,
            }
            for ve in championship.vehicles
        ],

        # Track statistics
        "track_stats": [
            {
                "track_name": ts.track_name,
                "track_file": ts.track_file,
                "class_records": [str(rec) for rec in ts.class_records],  # Convert tuples to strings
            }
            for ts in championship.track_stats
        ],

        # Career statistics
        "career_stats": {
            "experience": championship.career.experience,
            "money": championship.career.money,
            "total_races": championship.career.total_races,
            "total_races_with_ai": championship.career.total_races_with_ai,
            "total_laps": championship.career.total_laps,
            "total_points_scored": championship.career.total_points_scored,
            "total_championships": championship.career.total_championships,
            "total_wins": championship.career.total_wins,
            "total_poles": championship.career.total_poles,
            "total_lap_records": championship.career.total_lap_records,
            "aborted_seasons": championship.career.aborted_seasons,
            "avg_start_position": championship.career.avg_start_position,
            "avg_finish_position": championship.career.avg_finish_position,
        } if championship.career else None,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_championship(championship_data: ChampionshipCreateSchema):
    """
    Create a new championship.

    Args:
        championship_data: Championship information

    Returns:
        Success message

    Raises:
        400: Championship already exists or validation error
    """
    service = get_championship_service()

    # Extract filename from name (sanitize)
    filename = championship_data.name.replace(" ", "").replace("/", "").replace("\\", "")

    # Check if championship already exists
    if service.exists(filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Championship '{filename}' already exists"
        )

    try:
        # For now, we'll create a simple championship
        # Full implementation would build complete Championship object
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Championship creation via API not yet fully implemented. Use demo scripts for now."
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create championship: {str(e)}"
        )


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_championship(name: str):
    """
    Delete a championship.

    Args:
        name: Name of the championship file (without .cch)

    Raises:
        404: Championship not found
    """
    service = get_championship_service()

    if not service.exists(name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Championship '{name}' not found"
        )

    try:
        service.delete(name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete championship: {str(e)}"
        )


@router.post("/{name}/duplicate", status_code=status.HTTP_201_CREATED)
async def duplicate_championship(name: str, new_name: str):
    """
    Duplicate an existing championship.

    Args:
        name: Name of the source championship
        new_name: Name for the duplicated championship

    Returns:
        Success message

    Raises:
        404: Source championship not found
        400: New name already exists
    """
    service = get_championship_service()

    if not service.exists(name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Championship '{name}' not found"
        )

    # Sanitize new name
    new_filename = new_name.replace(" ", "").replace("/", "").replace("\\", "")

    if service.exists(new_filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Championship '{new_filename}' already exists"
        )

    try:
        service.duplicate(name, new_filename)
        return {"message": f"Championship duplicated successfully as '{new_filename}'"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to duplicate championship: {str(e)}"
        )
