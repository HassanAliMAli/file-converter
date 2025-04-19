import uuid
import shutil
import logging
from pathlib import Path
from typing import Annotated, List
import mimetypes

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    status,
    Query,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.config import settings
from app.core.security import current_active_verified_user
from app.db.session import get_db
from app.models.conversion import Conversion as ConversionModel, ConversionStatus
from app.models.file import File as FileModel
from app.models.user import User
from app.worker.tasks import process_file_conversion
from fastapi.responses import FileResponse, RedirectResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Use configured temporary directory
TEMP_UPLOAD_DIR = Path(settings.TEMP_DIR)
TEMP_UPLOAD_DIR.mkdir(exist_ok=True)


@router.post(
    "/upload",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload File for Conversion",
    response_description="Conversion task accepted",
)
async def upload_file(
    # Use Annotated for clearer dependency injection and parameter metadata
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_active_verified_user)],
    output_format: Annotated[
        str, Depends(lambda output_format: output_format.lower())
    ], # Normalize output format early
    file: Annotated[
        UploadFile,
        File(
            ...,
            description=f"File to upload (Max: {settings.MAX_UPLOAD_SIZE / 1024 / 1024:.1f} MB, Types: {', '.join(sorted(list(settings.parsed_allowed_content_types)))})",
        ),
    ],
):
    """
    Receives a file, validates it based on configured settings, saves it temporarily,
    creates corresponding database records for the file and the conversion job,
    and queues a background task to perform the actual conversion.
    """

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided",
        )

    # --- Input Validation ---
    if file.content_type not in settings.parsed_allowed_content_types:
        logger.warning(
            f"Upload rejected for user {current_user.id}. Invalid content type: {file.content_type}"
        )
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: '{file.content_type}'. Allowed: {', '.join(sorted(list(settings.parsed_allowed_content_types)))}",
        )

    if output_format not in settings.parsed_supported_output_formats:
        logger.warning(
            f"Upload rejected for user {current_user.id}. Invalid output format: {output_format}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported output format: '{output_format}'. Supported: {', '.join(sorted(list(settings.parsed_supported_output_formats)))}",
        )

    # --- File Saving & DB Record Creation ---
    stored_file_id = uuid.uuid4()
    # Basic sanitization: only use the filename part, ignore potential paths
    original_filename = Path(file.filename).name
    # Using stored_file_id ensures uniqueness if filenames clash and avoids issues with weird chars
    temp_file_path = TEMP_UPLOAD_DIR / str(stored_file_id)
    db_file = None
    db_conversion = None

    try:
        # Save the uploaded file (reading in chunks)
        logger.debug(
            f"Saving uploaded file '{original_filename}' to {temp_file_path}"
        )
        file_size = 0
        try:
            with temp_file_path.open("wb") as buffer:
                while chunk := await file.read(8192):  # Read in 8KB chunks
                    buffer.write(chunk)
                    file_size += len(chunk)

            # Double check size against limit (FastAPI/Starlette should catch it earlier via File())
            if file_size > settings.MAX_UPLOAD_SIZE:
                # This should ideally not be reached if File() validation works
                logger.error(
                    f"File size {file_size} exceeded limit {settings.MAX_UPLOAD_SIZE} after saving (potential race condition or bug?)."
                )
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE / 1024 / 1024:.1f} MB",
                )
        except Exception as save_exc:
            logger.error(
                f"Failed to save file {original_filename} to {temp_file_path}: {save_exc}",
                exc_info=True,
            )
            # Attempt cleanup if save fails partially
            temp_file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save uploaded file.",
            )

        logger.info(
            f"File '{original_filename}' (ID: {stored_file_id}) uploaded by user {current_user.id} to {temp_file_path}, size: {file_size} bytes"
        )

        # Create File record in DB
        db_file = FileModel(
            id=stored_file_id,
            original_filename=original_filename,
            storage_path=str(temp_file_path.resolve()),  # Store resolved path for now
            content_type=file.content_type,
            file_size=file_size,
            owner_id=current_user.id,
        )
        db.add(db_file)

        # Create Conversion record in DB
        db_conversion = ConversionModel(
            original_file_id=db_file.id,
            output_format=output_format, # Already normalized
            status=ConversionStatus.PENDING,
        )
        db.add(db_conversion)

        # Flush to get the conversion ID before queuing the task
        await db.flush()
        conversion_uuid = db_conversion.id # Fetch the generated UUID
        if not conversion_uuid:
             # This should not happen with UUID default, but defensively check
             raise SQLAlchemyError("Failed to get conversion ID after flush.")

        logger.info(
            f"Conversion job (ID: {conversion_uuid}) created for output format {output_format}"
        )

        # --- Task Queuing ---
        logger.debug(
            f"Queuing Celery task for conversion_id: {conversion_uuid}"
        )
        task = process_file_conversion.delay(
            conversion_id=str(conversion_uuid) # Pass UUID as string
        )
        logger.info(
            f"Conversion task {task.id} queued for {original_filename}"
        )

        # Update Conversion record with task_id
        db_conversion.task_id = task.id
        db.add(db_conversion) # Add again to mark for update

        # --- Final Commit ---
        await db.commit()
        logger.debug(
            f"DB changes committed for file {db_file.id} and conversion {db_conversion.id}"
        )

        return {
            "message": "File uploaded successfully, conversion started.",
            "task_id": task.id,
            "conversion_id": conversion_uuid, # Also return conversion ID
        }

    except SQLAlchemyError as db_exc:
        logger.error(
            f"Database error during file upload for {original_filename}: {db_exc}",
            exc_info=True,
        )
        await db.rollback()
        # Clean up the saved file if DB fails before commit
        temp_file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error during upload process.",
        )
    except Exception as e:
        # Catch any other unexpected error
        logger.error(
            f"Unexpected error during file upload for {original_filename} for user {current_user.id}: {e}",
            exc_info=True,
        )
        await db.rollback()
        # Clean up the saved file if error occurs before commit
        temp_file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file upload: {e}",
        )
    finally:
        # Ensure the UploadFile resource is closed to release temp resources
        await file.close()


@router.get("/status/{conversion_id}", summary="Get Conversion Status")
async def get_conversion_status(
    conversion_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_active_verified_user)],
):
    """Retrieves the status and details of a specific conversion job."""
    stmt = (
        select(ConversionModel)
        .options(joinedload(ConversionModel.original_file)) # Eager load file details
        .where(ConversionModel.id == conversion_id)
    )
    result = await db.execute(stmt)
    conversion = result.scalar_one_or_none()

    if not conversion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversion job not found")

    # Ensure the user owns the original file
    if conversion.original_file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this conversion status")

    return {
        "conversion_id": conversion.id,
        "task_id": conversion.task_id,
        "status": conversion.status,
        "output_format": conversion.output_format,
        "converted_file_path": conversion.converted_file_path,
        "error_message": conversion.error_message,
        "created_at": conversion.created_at,
        "updated_at": conversion.updated_at,
        "original_filename": conversion.original_file.original_filename,
    }

# TODO: Decide on download strategy: FileResponse vs redirect/signed URL
@router.get("/download/{conversion_id}", summary="Download Converted File")
async def download_converted_file(
    conversion_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_active_verified_user)],
):
    """Downloads the result of a completed conversion job."""
    stmt = (
        select(ConversionModel)
        .options(joinedload(ConversionModel.original_file)) # Need owner_id
        .where(ConversionModel.id == conversion_id)
    )
    result = await db.execute(stmt)
    conversion = result.scalar_one_or_none()

    if not conversion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversion job not found")

    # Ensure the user owns the original file
    if conversion.original_file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to download this file")

    if conversion.status != ConversionStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Conversion status is {conversion.status}, not COMPLETED.")

    if not conversion.converted_file_path:
        logger.error(f"Conversion {conversion_id} is COMPLETED but has no converted_file_path.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Converted file path not found.")

    # --- Download Strategy --- 
    # The strategy is to serve the file directly using FileResponse,
    # assuming the converted_file_path is locally accessible to the API server.
    # Ensure path is secure and within allowed directories (path traversal is prevented by Path conversion)
    local_file_path = Path(conversion.converted_file_path)
    if local_file_path.is_file(): # Basic check
         # Construct a user-friendly download filename
        base_name = Path(conversion.original_file.original_filename).stem
        # Sanitize base_name if necessary (though Path operations are generally safe)
        safe_base_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in base_name)
        download_filename = f"{safe_base_name}_converted.{conversion.output_format}"
        
        # Determine appropriate media type based on output format if possible
        # Using octet-stream is a safe default
        media_type = mimetypes.guess_type(download_filename)[0] or "application/octet-stream"
        
        logger.info(f"Serving file {local_file_path} as {download_filename} with type {media_type}")
        return FileResponse(local_file_path, media_type=media_type, filename=download_filename)
    else:
        # If the file path exists but isn't a file, or doesn't exist at all
        logger.error(f"Converted file path not found or invalid on server: {conversion.converted_file_path}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Converted file not available for download.")

# --- Add Conversion History Endpoint ---
@router.get("/",
    summary="Get User's Conversion History",
    response_model=List[ConversionStatusResponse] # Reuse the status response model
)
async def get_conversion_history(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(current_active_verified_user)],
    skip: Annotated[int, Query(ge=0, description="Number of records to skip for pagination")] = 0,
    limit: Annotated[int, Query(gt=0, le=100, description="Maximum number of records to return")] = 20 # Default limit 20, max 100
):
    """Retrieves a paginated list of conversion jobs initiated by the current user."""
    stmt = (
        select(ConversionModel)
        .join(ConversionModel.original_file) # Join with File to filter by owner
        .where(FileModel.owner_id == current_user.id)
        .order_by(ConversionModel.created_at.desc()) # Show newest first
        .offset(skip) # Apply pagination offset
        .limit(limit)  # Apply pagination limit
        .options(joinedload(ConversionModel.original_file)) # Eager load details needed for response
    )
    result = await db.execute(stmt)
    conversions = result.scalars().all()
    
    # Manually construct the response data to match ConversionStatusResponse structure
    # (Alternatively, define a Pydantic schema specifically for the list response)
    history = [
        {
            "conversion_id": conv.id,
            "task_id": conv.task_id,
            "status": conv.status.value, # Use enum value
            "output_format": conv.output_format,
            "converted_file_path": conv.converted_file_path,
            "error_message": conv.error_message,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "original_filename": conv.original_file.original_filename
        }
        for conv in conversions
    ]

    return history
# --- End Conversion History Endpoint --- 