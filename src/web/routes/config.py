"""API routes for configuration management."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ...utils.config import get_config
from ...utils.rfactor_validator import RFactorValidator

router = APIRouter()


class ConfigResponseSchema(BaseModel):
    """Schema for configuration response."""
    is_configured: bool
    rfactor_path: str | None = None
    current_player: str | None = None


class ConfigUpdateSchema(BaseModel):
    """Schema for configuration update."""
    rfactor_path: str
    current_player: str


@router.get("/", response_model=ConfigResponseSchema)
async def get_configuration():
    """
    Get current configuration.

    Returns:
        Current configuration
    """
    config = get_config()

    return ConfigResponseSchema(
        is_configured=config.is_configured(),
        rfactor_path=config.get_rfactor_path() if config.is_configured() else None,
        current_player=config.get_current_player() if config.is_configured() else None
    )


@router.put("/", response_model=ConfigResponseSchema)
async def update_configuration(config_data: ConfigUpdateSchema):
    """
    Update configuration.

    Args:
        config_data: New configuration

    Returns:
        Updated configuration

    Raises:
        400: Invalid rFactor path or player
    """
    config = get_config()

    # Validate rFactor path
    is_valid, errors = RFactorValidator.validate(config_data.rfactor_path)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid rFactor path: {', '.join(errors)}"
        )

    # Validate player
    players = RFactorValidator.list_player_profiles(config_data.rfactor_path)
    if config_data.current_player not in players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player '{config_data.current_player}' not found. Available players: {', '.join(players)}"
        )

    try:
        # Update configuration
        config.set_rfactor_path(config_data.rfactor_path, validate=True)
        config.set_current_player(config_data.current_player)

        return ConfigResponseSchema(
            is_configured=True,
            rfactor_path=config_data.rfactor_path,
            current_player=config_data.current_player
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update configuration: {str(e)}"
        )


@router.get("/players")
async def list_players(rfactor_path: str):
    """
    List available player profiles for a given rFactor path.

    Args:
        rfactor_path: Path to rFactor installation

    Returns:
        List of player profiles

    Raises:
        400: Invalid rFactor path
    """
    is_valid, errors = RFactorValidator.validate(rfactor_path)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid rFactor path: {', '.join(errors)}"
        )

    players = RFactorValidator.list_player_profiles(rfactor_path)
    return {"players": players}


@router.get("/validate")
async def validate_rfactor_path(path: str):
    """
    Validate an rFactor installation path.

    Args:
        path: Path to validate

    Returns:
        Validation result

    """
    is_valid, errors = RFactorValidator.validate(path)

    return {
        "is_valid": is_valid,
        "errors": errors
    }
