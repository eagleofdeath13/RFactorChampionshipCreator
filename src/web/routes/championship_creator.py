"""API routes for custom championship creation."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from pathlib import Path

from ..schemas.championship_creator import (
    CustomChampionshipCreateSchema,
    CustomChampionshipCreateResponseSchema,
    CustomChampionshipListSchema,
)
from ...services.championship_creator import ChampionshipCreator
from ...utils.config import get_config

router = APIRouter()


def get_championship_creator() -> ChampionshipCreator:
    """Get ChampionshipCreator instance."""
    config = get_config()
    if not config.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not configured. Please configure rFactor path first."
        )
    return ChampionshipCreator(config.get_rfactor_path())


@router.get("/custom", response_model=List[CustomChampionshipListSchema])
async def list_custom_championships():
    """
    List all custom championships created by the tool.

    Returns a list of all RFTOOL_* championships.
    """
    creator = get_championship_creator()
    championships = creator.isolation_service.list_isolated_championships()

    config = get_config()
    rfactor_path = Path(config.get_rfactor_path())
    rfm_dir = rfactor_path / "rFm"

    return [
        CustomChampionshipListSchema(
            name=name,
            full_name=f"RFTOOL_{name}",
            rfm_file=f"RFTOOL_{name}.rfm"
        )
        for name in championships
        if (rfm_dir / f"RFTOOL_{name}.rfm").exists()
    ]


@router.post("/custom", status_code=status.HTTP_201_CREATED, response_model=CustomChampionshipCreateResponseSchema)
async def create_custom_championship(data: CustomChampionshipCreateSchema):
    """
    Create a new custom championship.

    This will:
    1. Validate the championship name (max 12 chars for RFTOOL_ prefix)
    2. Isolate selected vehicles with driver assignments
    3. Copy all technical dependencies (.tbc, .ini, .pm, .mas)
    4. Generate the RFM file with proper settings
    5. Set StartingMoney to 500,000,000

    Args:
        data: Championship creation data

    Returns:
        Championship creation response with file paths

    Raises:
        400: Validation error or championship already exists
        500: Internal error during creation
    """
    creator = get_championship_creator()

    # Prepare vehicle assignments
    vehicle_assignments = [
        {
            'vehicle_path': va.vehicle_path,
            'driver_name': va.driver_name
        }
        for va in data.vehicle_assignments
    ]

    # Prepare options
    options = {}
    if data.full_name:
        options['full_name'] = data.full_name

    try:
        # Create championship
        rfm_path = creator.create_championship(
            championship_name=data.name,
            vehicle_assignments=vehicle_assignments,
            tracks=data.tracks,
            options=options
        )

        # Build response
        config = get_config()
        rfactor_path = Path(config.get_rfactor_path())
        vehicles_dir = rfactor_path / "GameData" / "Vehicles" / f"RFTOOL_{data.name}"

        return CustomChampionshipCreateResponseSchema(
            message="Championship created successfully",
            championship_name=data.name,
            rfm_file=rfm_path,
            vehicles_dir=str(vehicles_dir),
            vehicle_count=len(data.vehicle_assignments),
            track_count=len(data.tracks)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except IOError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create championship: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.delete("/custom/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_custom_championship(name: str):
    """
    Delete a custom championship.

    This will remove:
    1. The RFM file (RFTOOL_{name}.rfm)
    2. The isolated vehicles directory (RFTOOL_{name}/)

    Args:
        name: Championship name (without RFTOOL_ prefix)

    Raises:
        404: Championship not found
        500: Deletion failed
    """
    creator = get_championship_creator()

    try:
        creator.delete_championship(name)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IOError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete championship: {str(e)}"
        )
