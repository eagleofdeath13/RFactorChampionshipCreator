"""Pydantic schemas for Championship API."""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChampionshipSeasonSchema(BaseModel):
    """Schema for championship season settings."""

    name: str = Field(..., min_length=1, max_length=200)
    gameopt_race_laps: int = Field(default=10, ge=1, le=999)
    gameopt_opponents: int = Field(default=5, ge=0, le=60)
    gameopt_ai_driverstrength: int = Field(default=90, ge=0, le=120)
    gameopt_damagemultiplier: int = Field(default=100, ge=0, le=200)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mon Championnat 2025",
                "gameopt_race_laps": 15,
                "gameopt_opponents": 10,
                "gameopt_ai_driverstrength": 95,
                "gameopt_damagemultiplier": 75
            }
        }


class ChampionshipOpponentSchema(BaseModel):
    """Schema for championship opponent."""

    name: str
    veh_file: str
    season_points: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jean Dupont",
                "veh_file": "GAMEDATA\\\\VEHICLES\\\\TEAM01\\\\CAR01.VEH",
                "season_points": 0
            }
        }


class ChampionshipCreateSchema(BaseModel):
    """Schema for creating a new championship."""

    name: str = Field(..., min_length=1, max_length=200)
    race_laps: int = Field(default=10, ge=1, le=999)
    ai_strength: int = Field(default=90, ge=0, le=120)
    opponents: List[str] = Field(default_factory=list)
    player_vehicle: str = Field(default="")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Championnat GT 2025",
                "race_laps": 20,
                "ai_strength": 95,
                "opponents": ["Driver 1", "Driver 2", "Driver 3"],
                "player_vehicle": "GAMEDATA\\\\VEHICLES\\\\PLAYER\\\\CAR.VEH"
            }
        }


class ChampionshipInfoSchema(BaseModel):
    """Schema for championship basic info."""

    filename: str
    name: str
    status: int
    player: str
    opponents: int
    current_race: int
    player_points: int
    type: Optional[str] = None  # 'RFM' or 'CCH'
    is_rfm: Optional[bool] = False  # True if this is an RFM file (championship definition)
    is_custom: Optional[bool] = False  # True if this is a custom RFTOOL_ championship
    num_tracks: Optional[int] = None  # Number of tracks in the championship

    class Config:
        json_schema_extra = {
            "example": {
                "filename": "MyChampionship",
                "name": "Mon Championnat 2025",
                "status": 1,
                "player": "Loic",
                "opponents": 10,
                "current_race": 3,
                "player_points": 45,
                "type": "CCH",
                "is_rfm": False,
                "is_custom": False,
                "num_tracks": 10
            }
        }


class ChampionshipDetailSchema(BaseModel):
    """Schema for detailed championship info."""

    name: str
    status: int
    race_laps: int
    ai_strength: int
    opponents_count: int
    player_name: str
    player_points: int
    current_race: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Mon Championnat 2025",
                "status": 1,
                "race_laps": 15,
                "ai_strength": 95,
                "opponents_count": 10,
                "player_name": "Loic",
                "player_points": 45,
                "current_race": 3
            }
        }
