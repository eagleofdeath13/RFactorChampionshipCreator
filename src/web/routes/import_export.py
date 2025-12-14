"""API routes for import/export functionality."""

from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse, StreamingResponse
from typing import List
import tempfile
import io
from pathlib import Path

from ...services.talent_service import TalentService
from ...services.import_service import ImportService
from ...utils.config import get_config

router = APIRouter()


def get_import_service() -> ImportService:
    """Get ImportService instance."""
    config = get_config()
    if not config.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not configured. Please configure rFactor path first."
        )
    talent_service = TalentService(config.get_rfactor_path())
    return ImportService(talent_service)


@router.post("/import/talents")
async def import_talents_csv(
    file: UploadFile = File(...),
    overwrite_existing: bool = True,
    fill_missing: bool = True,
    validate_only: bool = False
):
    """
    Import talents from CSV file.

    Args:
        file: CSV file to import
        overwrite_existing: Overwrite talents that already exist (default: True)
        fill_missing: Use randomizer to fill missing/empty fields (default: True)
        validate_only: Only validate without creating files

    Returns:
        Import result with success/error/warning counts

    Raises:
        400: Invalid file or validation error

    Notes:
        - If overwrite_existing=True, existing talents will be updated with CSV data
        - If fill_missing=True, empty/missing fields will be randomly generated
        - Warnings are issued for overwritten talents
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )

    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        # Import from CSV
        import_service = get_import_service()
        result = import_service.import_from_csv(
            temp_path,
            overwrite_existing=overwrite_existing,
            fill_missing=fill_missing,
            validate_only=validate_only
        )

        # Clean up temp file
        Path(temp_path).unlink()

        # Format errors for response
        errors = [
            {
                "row": row_num,
                "name": name,
                "message": error
            }
            for row_num, name, error in result.errors
        ]

        # Format warnings for response
        warnings = [
            {
                "row": row_num,
                "name": name,
                "message": warning
            }
            for row_num, name, warning in result.warnings
        ]

        return {
            "success_count": result.success_count,
            "error_count": result.error_count,
            "overwrite_count": result.overwrite_count,
            "total": result.total,
            "errors": errors,
            "warnings": warnings
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}"
        )


@router.post("/import/validate")
async def validate_talents_csv(file: UploadFile = File(...)):
    """
    Validate a CSV file without importing.

    Args:
        file: CSV file to validate

    Returns:
        Validation result

    Raises:
        400: Invalid file
    """
    return await import_talents_csv(file, overwrite_existing=True, fill_missing=True, validate_only=True)


@router.get("/export/talents")
async def export_talents_csv(talent_names: List[str] = None):
    """
    Export talents to CSV file.

    Args:
        talent_names: Optional list of talent names to export (all if not specified)

    Returns:
        CSV file download

    Raises:
        400: Invalid talent names
    """
    try:
        import_service = get_import_service()

        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as temp_file:
            temp_path = temp_file.name

        # Export to temp file
        if talent_names:
            import_service.export_to_csv(temp_path, talent_names=talent_names)
        else:
            import_service.export_to_csv(temp_path)

        # Read file content
        with open(temp_path, 'rb') as f:
            content = f.read()

        # Clean up
        Path(temp_path).unlink()

        # Return as download
        return StreamingResponse(
            io.BytesIO(content),
            media_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=talents_export.csv'}
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )


@router.get("/template/talents")
async def get_talents_template():
    """
    Download a CSV template for talent import.

    Returns:
        CSV template file
    """
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as temp_file:
            temp_path = temp_file.name

        # Generate template
        ImportService.generate_csv_template(temp_path)

        # Read file content
        with open(temp_path, 'rb') as f:
            content = f.read()

        # Clean up
        Path(temp_path).unlink()

        # Return as download
        return StreamingResponse(
            io.BytesIO(content),
            media_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=talents_template.csv'}
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Template generation failed: {str(e)}"
        )
