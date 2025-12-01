"""
Pydantic schemas for track API endpoints.
"""

from pydantic import BaseModel, Field


class TrackListItemSchema(BaseModel):
    file_name: str = Field(description="Filename")
    relative_path: str = Field(description="Path relative to GameData/Locations")
    display_name: str = Field(description="Display-friendly track name")
    venue_name: str = Field(default="", description="Venue/Location")
    layout: str = Field(default="", description="Layout name")


class TrackResponseSchema(BaseModel):
    track_name: str = Field(description="Track name")
    venue_name: str = Field(description="Venue name")
    layout: str = Field(description="Layout name")
    file_path: str = Field(description="Full path to .gdb file")
    file_name: str = Field(description="Filename")
    relative_path: str = Field(description="Path relative to GameData/Locations")
    display_name: str = Field(description="Display-friendly track name")
    gdb_info: dict[str, str] | None = Field(default=None, description="All key=value pairs parsed from GDB")
