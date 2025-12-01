"""API routes for tracks (circuits) management."""

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional

from ..schemas.track import TrackListItemSchema, TrackResponseSchema
from ...services.track_service import TrackService


router = APIRouter()


def _track_to_list_item(track) -> TrackListItemSchema:
    return TrackListItemSchema(
        file_name=track.file_name,
        relative_path=track.relative_path,
        display_name=track.display_name,
        venue_name=track.venue_name,
        layout=track.layout,
    )


def _track_to_response(track) -> TrackResponseSchema:
    return TrackResponseSchema(
        track_name=track.track_name,
        venue_name=track.venue_name,
        layout=track.layout,
        file_path=track.file_path,
        file_name=track.file_name,
        relative_path=track.relative_path,
        display_name=track.display_name,
        gdb_info=getattr(track, "gdb_info", None) or None,
    )


@router.get("/", response_model=List[TrackListItemSchema])
async def list_tracks(
    search: Optional[str] = Query(None, description="Search by name/venue/layout"),
    reload: bool = Query(False, description="Force reload from disk"),
):
    service = TrackService()
    try:
        if search:
            tracks = service.search(search, force_reload=reload)
        else:
            tracks = service.list_all(force_reload=reload)
        return [_track_to_list_item(t) for t in tracks]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{path:path}", response_model=TrackResponseSchema)
async def get_track(path: str):
    service = TrackService()
    try:
        track = service.get_by_relative_path(path)
        if not track:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Circuit introuvable")
        return _track_to_response(track)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
