"""
Pydantic schemas for vehicle API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class VehicleTeamInfoSchema(BaseModel):
    """Schema for vehicle team information."""

    team: str = Field(default="", description="Team name")
    full_team_name: str = Field(default="", description="Full team name")
    driver: str = Field(default="", description="Driver name")
    pit_group: str = Field(default="Group1", description="Pit group")
    team_founded: Optional[int] = Field(default=None, description="Year team was founded")
    team_headquarters: str = Field(default="", description="Team headquarters location")
    team_starts: int = Field(default=0, ge=0, description="Number of starts")
    team_poles: int = Field(default=0, ge=0, description="Number of pole positions")
    team_wins: int = Field(default=0, ge=0, description="Number of wins")
    team_world_championships: int = Field(default=0, ge=0, description="Number of world championships")

    class Config:
        json_schema_extra = {
            "example": {
                "team": "Howston Team Campana Racing",
                "full_team_name": "Campana Racing",
                "driver": "Joe Campana",
                "pit_group": "Group1",
                "team_founded": 2005,
                "team_headquarters": "Plymouth, Michigan",
                "team_starts": 0,
                "team_poles": 0,
                "team_wins": 0,
                "team_world_championships": 0
            }
        }


class VehicleConfigSchema(BaseModel):
    """Schema for vehicle technical configuration."""

    default_livery: str = Field(default="", description="Default livery file")
    hdvehicle: str = Field(default="", description="HDV file reference")
    hdvehicle_resolved: str = Field(default="", description="Resolved absolute path to HDV (if available)")
    hdvehicle_exists: bool = Field(default=False, description="Whether the resolved HDV file exists on disk")
    graphics: str = Field(default="", description="Graphics file reference")
    spinner: str = Field(default="", description="Spinner file reference")
    upgrades: str = Field(default="", description="Upgrades file reference")
    sounds: str = Field(default="", description="Sounds file reference")
    cameras: str = Field(default="", description="Cameras file reference")
    head_physics: str = Field(default="", description="Head physics file reference")
    cockpit: str = Field(default="", description="Cockpit file reference")
    ai_upgrade_class: str = Field(default="", description="AI upgrade class")

    class Config:
        json_schema_extra = {
            "example": {
                "default_livery": "Campana_27.DDS",
                "hdvehicle": "HW.hdv",
                "hdvehicle_resolved": "C:/Games/rFactor/GameData/Vehicles/Howston/HW.hdv",
                "hdvehicle_exists": True,
                "graphics": "HW_upgrades.gen",
                "spinner": "HW_Spinner.gen",
                "upgrades": "HW_Upgrades.ini",
                "sounds": "Howston.sfx",
                "cameras": "Howston_cams.cam",
                "head_physics": "headphysics.ini",
                "cockpit": "HW_cockpitinfo.ini",
                "ai_upgrade_class": "GP3"
            }
        }


class VehicleResponseSchema(BaseModel):
    """Schema for vehicle response (full details)."""

    number: int = Field(description="Vehicle number")
    description: str = Field(description="Vehicle description")
    engine: str = Field(description="Engine name/type")
    manufacturer: str = Field(description="Manufacturer name")
    classes: str = Field(description="Vehicle classes (space-separated)")
    category: str = Field(description="Vehicle category")
    team_info: VehicleTeamInfoSchema = Field(description="Team and driver information")
    config: VehicleConfigSchema = Field(description="Technical configuration")
    file_path: str = Field(description="Full path to .veh file")
    file_name: str = Field(description="Filename")
    relative_path: str = Field(description="Path relative to GameData/Vehicles")
    display_name: str = Field(description="Display-friendly name")
    class_list: list[str] = Field(description="Vehicle classes as a list")

    class Config:
        json_schema_extra = {
            "example": {
                "number": 27,
                "description": "Campana #27",
                "engine": "ISM",
                "manufacturer": "H6",
                "classes": "SRGP 2005 Howston GP3 NO_AI",
                "category": "H6,2005 Howston",
                "team_info": {
                    "team": "Howston Team Campana Racing",
                    "driver": "Joe Campana"
                },
                "config": {
                    "default_livery": "Campana_27.DDS",
                    "hdvehicle": "HW.hdv"
                },
                "file_name": "Campana_27.veh",
                "relative_path": "Howston/SRGP/Campana/Campana_27.veh",
                "display_name": "Campana #27",
                "class_list": ["SRGP", "2005", "Howston", "GP3", "NO_AI"]
            }
        }


class VehicleListItemSchema(BaseModel):
    """Schema for vehicle in list view (summary)."""

    file_name: str = Field(description="Filename")
    relative_path: str = Field(description="Path relative to GameData/Vehicles")
    display_name: str = Field(description="Display-friendly name")
    number: int = Field(description="Vehicle number")
    driver: str = Field(description="Driver name")
    team: str = Field(description="Team name")
    manufacturer: str = Field(description="Manufacturer")
    classes: str = Field(description="Vehicle classes")

    class Config:
        json_schema_extra = {
            "example": {
                "file_name": "Campana_27.veh",
                "relative_path": "Howston/SRGP/Campana/Campana_27.veh",
                "display_name": "Campana #27",
                "number": 27,
                "driver": "Joe Campana",
                "team": "Howston Team Campana Racing",
                "manufacturer": "H6",
                "classes": "SRGP 2005 Howston GP3"
            }
        }


class VehicleClassSchema(BaseModel):
    """Schema for vehicle class information."""

    class_name: str = Field(description="Class name")
    count: int = Field(description="Number of vehicles in this class", ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "class_name": "SRGP",
                "count": 45
            }
        }


class VehicleManufacturerSchema(BaseModel):
    """Schema for manufacturer information."""

    manufacturer: str = Field(description="Manufacturer name")
    count: int = Field(description="Number of vehicles from this manufacturer", ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "manufacturer": "H6",
                "count": 30
            }
        }
