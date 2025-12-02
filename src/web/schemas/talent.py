"""Pydantic schemas for Talent API."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class TalentPersonalInfoSchema(BaseModel):
    """Schema for talent personal information."""

    nationality: str = Field(..., min_length=1, max_length=100)
    date_of_birth: str = Field(..., pattern=r'^\d{1,2}-\d{1,2}-\d{4}$')  # Allow 1 or 2 digits for day/month
    starts: int = Field(default=0, ge=0)
    poles: int = Field(default=0, ge=0)
    wins: int = Field(default=0, ge=0)
    drivers_championships: int = Field(default=0, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "nationality": "France",
                "date_of_birth": "15-03-1990",
                "starts": 100,
                "poles": 10,
                "wins": 5,
                "drivers_championships": 1
            }
        }


class TalentStatsSchema(BaseModel):
    """Schema for talent racing statistics."""

    aggression: float = Field(default=50.0, ge=0.0, le=100.0)
    reputation: float = Field(default=50.0, ge=0.0, le=100.0)
    courtesy: float = Field(default=50.0, ge=0.0, le=100.0)
    composure: float = Field(default=50.0, ge=0.0, le=100.0)
    speed: float = Field(default=50.0, ge=0.0, le=100.0)
    crash: float = Field(default=50.0, ge=0.0, le=100.0)
    recovery: float = Field(default=50.0, ge=0.0, le=100.0)
    completed_laps: float = Field(default=90.0, ge=0.0, le=100.0)
    min_racing_skill: float = Field(default=50.0, ge=0.0, le=100.0)

    class Config:
        json_schema_extra = {
            "example": {
                "aggression": 75.0,
                "reputation": 80.0,
                "courtesy": 70.0,
                "composure": 85.0,
                "speed": 90.0,
                "crash": 30.0,
                "recovery": 75.0,
                "completed_laps": 95.0,
                "min_racing_skill": 80.0
            }
        }


class TalentCreateSchema(BaseModel):
    """Schema for creating a new talent."""

    name: str = Field(..., min_length=1, max_length=200)
    personal_info: TalentPersonalInfoSchema
    stats: TalentStatsSchema

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jean Dupont",
                "personal_info": {
                    "nationality": "France",
                    "date_of_birth": "15-03-1990",
                    "starts": 100,
                    "poles": 10,
                    "wins": 5,
                    "drivers_championships": 1
                },
                "stats": {
                    "aggression": 75.0,
                    "speed": 90.0,
                    "composure": 85.0
                }
            }
        }


class TalentUpdateSchema(BaseModel):
    """Schema for updating an existing talent."""

    personal_info: Optional[TalentPersonalInfoSchema] = None
    stats: Optional[TalentStatsSchema] = None

    class Config:
        json_schema_extra = {
            "example": {
                "stats": {
                    "speed": 95.0,
                    "aggression": 80.0
                }
            }
        }


class TalentResponseSchema(BaseModel):
    """Schema for talent response."""

    name: str
    personal_info: TalentPersonalInfoSchema
    stats: TalentStatsSchema
    file_path: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Jean Dupont",
                "personal_info": {
                    "nationality": "France",
                    "date_of_birth": "15-03-1990",
                    "starts": 100,
                    "poles": 10,
                    "wins": 5,
                    "drivers_championships": 1
                },
                "stats": {
                    "aggression": 75.0,
                    "reputation": 80.0,
                    "courtesy": 70.0,
                    "composure": 85.0,
                    "speed": 90.0,
                    "crash": 30.0,
                    "recovery": 75.0,
                    "completed_laps": 95.0,
                    "min_racing_skill": 80.0
                },
                "file_path": "C:\\rFactor\\GameData\\Talent\\JeanDupont.rcd"
            }
        }


class TalentListItemSchema(BaseModel):
    """Schema for talent list item (minimal info)."""

    name: str
    nationality: str
    speed: float
    crash: float = Field(default=50.0, ge=0.0, le=100.0)
    aggression: float = Field(default=50.0, ge=0.0, le=100.0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jean Dupont",
                "nationality": "France",
                "speed": 90.0,
                "crash": 30.0,
                "aggression": 75.0
            }
        }
