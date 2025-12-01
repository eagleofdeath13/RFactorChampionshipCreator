"""Pydantic schemas for Custom Championship Creation API."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class VehicleAssignmentSchema(BaseModel):
    """Schema for vehicle-driver assignment."""

    vehicle_path: str = Field(
        ...,
        description="Relative path to vehicle file (e.g., 'RHEZ/2005RHEZ/SRGP/TEAM BLACK/BLK_03.veh')"
    )
    driver_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the driver to assign to this vehicle"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_path": "RHEZ/2005RHEZ/SRGP/TEAM BLACK/BLK_03.veh",
                "driver_name": "John Doe"
            }
        }


class CustomChampionshipCreateSchema(BaseModel):
    """Schema for creating a new custom championship."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=12,  # Limit for RFTOOL_ prefix (19 - 7 = 12)
        description="Championship name (max 12 chars for RFTOOL_ prefix compatibility)"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=50,
        description="Full championship name (optional, defaults to name)"
    )
    vehicle_assignments: List[VehicleAssignmentSchema] = Field(
        ...,
        min_length=1,
        description="List of vehicle-driver assignments"
    )
    tracks: List[str] = Field(
        ...,
        min_length=1,
        description="List of track names in race order"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate championship name is alphanumeric with underscores only."""
        if not v.replace('_', '').isalnum():
            raise ValueError('Championship name must be alphanumeric (underscores allowed)')
        return v

    @field_validator('vehicle_assignments')
    @classmethod
    def validate_vehicle_assignments(cls, v: List[VehicleAssignmentSchema]) -> List[VehicleAssignmentSchema]:
        """Validate at least one vehicle assignment."""
        if not v:
            raise ValueError('At least one vehicle assignment is required')
        return v

    @field_validator('tracks')
    @classmethod
    def validate_tracks(cls, v: List[str]) -> List[str]:
        """Validate at least one track."""
        if not v:
            raise ValueError('At least one track is required')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "TC2025",
                "full_name": "Test Championship 2025",
                "vehicle_assignments": [
                    {
                        "vehicle_path": "RHEZ/2005RHEZ/SRGP/TEAM BLACK/BLK_03.veh",
                        "driver_name": "Driver Black"
                    },
                    {
                        "vehicle_path": "RHEZ/2005RHEZ/SRGP/TEAM RED/RD_01.veh",
                        "driver_name": "Driver Red"
                    },
                    {
                        "vehicle_path": "ZR/SRGP/TEAM_GREEN/GRN_08.veh",
                        "driver_name": "Driver Green"
                    }
                ],
                "tracks": [
                    "Mills_Short",
                    "Joesville_Speedway",
                    "Toban_Short"
                ]
            }
        }


class CustomChampionshipCreateResponseSchema(BaseModel):
    """Response schema for championship creation."""

    message: str
    championship_name: str
    rfm_file: str
    vehicles_dir: str
    vehicle_count: int
    track_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Championship created successfully",
                "championship_name": "TC2025",
                "rfm_file": "C:\\rFactor\\rFm\\RFTOOL_TC2025.rfm",
                "vehicles_dir": "C:\\rFactor\\GameData\\Vehicles\\RFTOOL_TC2025",
                "vehicle_count": 3,
                "track_count": 3
            }
        }


class CustomChampionshipListSchema(BaseModel):
    """Schema for listing custom championships."""

    name: str
    full_name: str
    rfm_file: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "TC2025",
                "full_name": "RFTOOL_TC2025",
                "rfm_file": "RFTOOL_TC2025.rfm"
            }
        }
