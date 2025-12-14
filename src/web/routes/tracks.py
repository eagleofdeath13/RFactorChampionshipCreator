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
    search: Optional[str] = Query(None, description="Search query"),
    search_track_name: bool = Query(True, description="Search in track name"),
    search_venue_name: bool = Query(True, description="Search in venue name"),
    search_layout: bool = Query(True, description="Search in layout"),
    search_file_name: bool = Query(True, description="Search in file name"),
    reload: bool = Query(False, description="Force reload from disk"),
):
    """
    List all tracks with advanced search options.

    Query parameters:
    - search: Search query (searches in selected fields)
    - search_track_name: Include track name in search (default: true)
    - search_venue_name: Include venue name in search (default: true)
    - search_layout: Include layout in search (default: true)
    - search_file_name: Include file name in search (default: true)
    - reload: Force reload from disk (default: false, uses cache)
    """
    service = TrackService()
    try:
        if search:
            tracks = service.search(
                search,
                search_track_name=search_track_name,
                search_venue_name=search_venue_name,
                search_layout=search_layout,
                search_file_name=search_file_name,
                force_reload=reload
            )
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
