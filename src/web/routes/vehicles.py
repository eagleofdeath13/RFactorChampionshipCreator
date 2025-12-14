"""API routes for vehicles management."""

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from dataclasses import asdict
from collections import Counter

from ..schemas.vehicle import (
    VehicleResponseSchema,
    VehicleListItemSchema,
    VehicleTeamInfoSchema,
    VehicleConfigSchema,
    VehicleClassSchema,
    VehicleManufacturerSchema,
    VehicleUpdateSchema,
)
from ...services.vehicle_service import VehicleService

router = APIRouter()


def _vehicle_to_response(vehicle) -> VehicleResponseSchema:
    """Convert Vehicle model to response schema."""
    return VehicleResponseSchema(
        number=vehicle.number,
        description=vehicle.description,
        engine=vehicle.engine,
        manufacturer=vehicle.manufacturer,
        classes=vehicle.classes,
        category=vehicle.category,
        team_info=VehicleTeamInfoSchema(**asdict(vehicle.team_info)),
        config=VehicleConfigSchema(**asdict(vehicle.config)),
        file_path=vehicle.file_path,
        file_name=vehicle.file_name,
        relative_path=vehicle.relative_path,
        display_name=vehicle.display_name,
        class_list=vehicle.class_list,
    )


def _vehicle_to_list_item(vehicle) -> VehicleListItemSchema:
    """Convert Vehicle model to list item schema."""
    return VehicleListItemSchema(
        file_name=vehicle.file_name,
        relative_path=vehicle.relative_path,
        display_name=vehicle.display_name,
        number=vehicle.number,
        driver=vehicle.team_info.driver,
        team=vehicle.team_info.team,
        manufacturer=vehicle.manufacturer,
        classes=vehicle.classes,
    )


@router.get("/", response_model=List[VehicleListItemSchema])
async def list_vehicles(
    vehicle_class: Optional[str] = Query(None, description="Filter by vehicle class"),
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer"),
    search: Optional[str] = Query(None, description="Search query"),
    search_driver: bool = Query(True, description="Search in driver name"),
    search_team: bool = Query(True, description="Search in team name"),
    search_description: bool = Query(True, description="Search in description"),
    reload: bool = Query(False, description="Force reload from disk"),
):
    """
    List all vehicles with advanced search options.

    Query parameters:
    - vehicle_class: Filter by vehicle class (e.g., "SRGP")
    - manufacturer: Filter by manufacturer
    - search: Search query (searches in selected fields)
    - search_driver: Include driver name in search (default: true)
    - search_team: Include team name in search (default: true)
    - search_description: Include description in search (default: true)
    - reload: Force reload from disk (default: false, uses cache)
    """
    service = VehicleService()

    try:
        # Get vehicles based on filters
        if vehicle_class:
            vehicles = service.filter_by_class(vehicle_class, force_reload=reload)
        elif manufacturer:
            vehicles = service.filter_by_manufacturer(manufacturer, force_reload=reload)
        elif search:
            vehicles = service.search(
                search,
                search_driver=search_driver,
                search_team=search_team,
                search_description=search_description,
                force_reload=reload
            )
        else:
            vehicles = service.list_all(force_reload=reload)

        # Convert to list items
        return [_vehicle_to_list_item(v) for v in vehicles]
    except ValueError as e:
        # Configuration problem
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        # Missing Vehicles directory
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/classes", response_model=List[VehicleClassSchema])
async def list_classes(reload: bool = Query(False, description="Force reload from disk")):
    """
    Get all vehicle classes with counts.

    Query parameters:
    - reload: Force reload from disk (default: false, uses cache)
    """
    service = VehicleService()
    try:
        vehicles = service.list_all(force_reload=reload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    # Count vehicles per class
    class_counts = Counter()
    for vehicle in vehicles:
        for class_name in vehicle.class_list:
            class_counts[class_name] += 1

    # Sort by count (descending) then name
    classes = [
        VehicleClassSchema(class_name=name, count=count)
        for name, count in sorted(class_counts.items(), key=lambda x: (-x[1], x[0]))
    ]

    return classes


@router.get("/manufacturers", response_model=List[VehicleManufacturerSchema])
async def list_manufacturers(reload: bool = Query(False, description="Force reload from disk")):
    """
    Get all manufacturers with counts.

    Query parameters:
    - reload: Force reload from disk (default: false, uses cache)
    """
    service = VehicleService()
    try:
        vehicles = service.list_all(force_reload=reload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    # Count vehicles per manufacturer
    manufacturer_counts = Counter()
    for vehicle in vehicles:
        if vehicle.manufacturer:
            manufacturer_counts[vehicle.manufacturer] += 1

    # Sort by count (descending) then name
    manufacturers = [
        VehicleManufacturerSchema(manufacturer=name, count=count)
        for name, count in sorted(manufacturer_counts.items(), key=lambda x: (-x[1], x[0]))
    ]

    return manufacturers


@router.get("/stats")
async def get_vehicle_stats(reload: bool = Query(False, description="Force reload from disk")):
    """
    Get vehicle statistics.

    Query parameters:
    - reload: Force reload from disk (default: false, uses cache)
    """
    service = VehicleService()
    vehicles = service.list_all(force_reload=reload)

    unique_classes = service.get_unique_classes(force_reload=reload)
    unique_manufacturers = service.get_unique_manufacturers(force_reload=reload)

    return {
        "total_vehicles": len(vehicles),
        "total_classes": len(unique_classes),
        "total_manufacturers": len(unique_manufacturers),
    }


@router.get("/{file_name:path}", response_model=VehicleResponseSchema)
async def get_vehicle(file_name: str):
    """
    Get a specific vehicle by filename or relative path.

    Parameters:
    - file_name: Vehicle filename (e.g., "Campana_27.veh") or relative path
      (e.g., "Howston/SRGP/Campana/Campana_27.veh")
    """
    service = VehicleService()
    try:
        # Try as filename first
        vehicle = service.get_by_filename(file_name)

        # If not found, try as relative path
        if not vehicle:
            vehicle = service.get_by_relative_path(file_name)

        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle '{file_name}' not found"
            )

        return _vehicle_to_response(vehicle)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/reload")
async def reload_vehicles():
    """
    Force reload all vehicles from disk (clear cache).

    This is useful after adding or modifying vehicle files.
    """
    service = VehicleService()
    service.clear_cache()
    vehicles = service.list_all(force_reload=True)

    return {
        "message": "Vehicles reloaded successfully",
        "total_vehicles": len(vehicles)
    }


@router.put("/{file_name:path}", response_model=VehicleResponseSchema)
async def update_vehicle(file_name: str, update_data: VehicleUpdateSchema):
    """
    Update a vehicle.

    Parameters:
    - file_name: Vehicle filename or relative path
    - update_data: Fields to update (currently supports: driver)

    Returns:
        Updated vehicle data
    """
    service = VehicleService()
    try:
        # Update the vehicle
        updated_vehicle = service.update(
            relative_path=file_name,
            driver=update_data.driver
        )

        return _vehicle_to_response(updated_vehicle)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating vehicle: {str(e)}"
        )
