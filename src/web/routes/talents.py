"""API routes for talents management."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from dataclasses import asdict

from ..schemas.talent import (
    TalentCreateSchema,
    TalentUpdateSchema,
    TalentResponseSchema,
    TalentListItemSchema,
    TalentPersonalInfoSchema,
    TalentStatsSchema,
)
from ...services.talent_service import TalentService
from ...models.talent import Talent, TalentPersonalInfo, TalentStats
from ...utils.config import get_config

router = APIRouter()


def get_talent_service() -> TalentService:
    """Get TalentService instance."""
    config = get_config()
    if not config.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not configured. Please configure rFactor path first."
        )
    return TalentService(config.get_rfactor_path())


@router.get("/", response_model=List[TalentListItemSchema])
async def list_talents():
    """
    List all talents.

    Returns a list of all available talents with basic information.
    """
    service = get_talent_service()
    talents = service.list_all_talents()

    return [
        TalentListItemSchema(
            name=talent.name,
            nationality=talent.personal_info.nationality,
            speed=talent.stats.speed
        )
        for talent in talents
    ]


@router.get("/{name}", response_model=TalentResponseSchema)
async def get_talent(name: str):
    """
    Get a specific talent by name.

    Args:
        name: Name of the talent

    Returns:
        Talent details

    Raises:
        404: Talent not found
    """
    service = get_talent_service()
    talent = service.get(name)

    if not talent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Talent '{name}' not found"
        )

    # Convert dataclasses to Pydantic models
    return TalentResponseSchema(
        name=talent.name,
        personal_info=TalentPersonalInfoSchema(**asdict(talent.personal_info)),
        stats=TalentStatsSchema(**asdict(talent.stats)),
        file_path=talent.file_path
    )


@router.post("/", response_model=TalentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_talent(talent_data: TalentCreateSchema):
    """
    Create a new talent.

    Args:
        talent_data: Talent information

    Returns:
        Created talent

    Raises:
        400: Talent already exists or validation error
    """
    service = get_talent_service()

    # Check if talent already exists
    if service.exists(talent_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Talent '{talent_data.name}' already exists"
        )

    try:
        # Create Talent object
        talent = Talent(
            name=talent_data.name,
            personal_info=TalentPersonalInfo(**talent_data.personal_info.model_dump()),
            stats=TalentStats(**talent_data.stats.model_dump())
        )

        # Save talent
        service.create(talent)

        # Reload to get file_path
        created = service.get(talent.name)

        return TalentResponseSchema(
            name=created.name,
            personal_info=TalentPersonalInfoSchema(**asdict(created.personal_info)),
            stats=TalentStatsSchema(**asdict(created.stats)),
            file_path=created.file_path
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create talent: {str(e)}"
        )


@router.put("/{name}", response_model=TalentResponseSchema)
async def update_talent(name: str, talent_data: TalentUpdateSchema):
    """
    Update an existing talent.

    Args:
        name: Name of the talent to update
        talent_data: Updated talent information

    Returns:
        Updated talent

    Raises:
        404: Talent not found
        400: Validation error
    """
    service = get_talent_service()

    # Get existing talent
    talent = service.get(name)
    if not talent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Talent '{name}' not found"
        )

    try:
        # Update fields if provided
        if talent_data.personal_info:
            talent.personal_info = TalentPersonalInfo(**talent_data.personal_info.model_dump())

        if talent_data.stats:
            talent.stats = TalentStats(**talent_data.stats.model_dump())

        # Save updated talent
        service.update(talent)

        # Reload
        updated = service.get(name)

        return TalentResponseSchema(
            name=updated.name,
            personal_info=TalentPersonalInfoSchema(**asdict(updated.personal_info)),
            stats=TalentStatsSchema(**asdict(updated.stats)),
            file_path=updated.file_path
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update talent: {str(e)}"
        )


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_talent(name: str):
    """
    Delete a talent.

    Args:
        name: Name of the talent to delete

    Raises:
        404: Talent not found
    """
    service = get_talent_service()

    if not service.exists(name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Talent '{name}' not found"
        )

    try:
        service.delete(name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete talent: {str(e)}"
        )


@router.get("/search/", response_model=List[TalentListItemSchema])
async def search_talents(q: str):
    """
    Search talents by name or nationality.

    Args:
        q: Search query

    Returns:
        List of matching talents
    """
    service = get_talent_service()
    talents = service.search(q)

    return [
        TalentListItemSchema(
            name=talent.name,
            nationality=talent.personal_info.nationality,
            speed=talent.stats.speed
        )
        for talent in talents
    ]
