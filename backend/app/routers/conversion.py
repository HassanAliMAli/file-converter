from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from pathlib import Path
import shutil
import logging
import uuid

from app.core.security import current_active_verified_user
from app.models import User
from app.worker.tasks import process_file_conversion

router = APIRouter()
logger = logging.getLogger(__name__)

# Define a temporary directory for uploads (consider making this configurable)
TEMP_UPLOAD_DIR = Path("temp_uploads")
TEMP_UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(
    file: UploadFile = File(...),
    output_format: str = "pdf", # Example: Get desired output format (needs refinement)
    current_user: User = Depends(current_active_verified_user)
):
    """Receives a file, saves it temporarily, and queues conversion task."""
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

    # Basic validation (add more robust checks based on PRD)
    allowed_content_types = ["image/jpeg", "image/png", "application/pdf", "text/plain"] # Example
    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {', '.join(allowed_content_types)}"
        )

    # Secure filename handling (consider using a library or more robust sanitization)
    safe_filename = f"{uuid.uuid4()}_{Path(file.filename).name}"
    temp_file_path = TEMP_UPLOAD_DIR / safe_filename

    try:
        # Save the uploaded file asynchronously
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File '{file.filename}' uploaded by user {current_user.id} to {temp_file_path}")

        # Queue the conversion task
        task = process_file_conversion.delay(
            input_file_path=str(temp_file_path.resolve()),
            output_format=output_format,
            original_filename=file.filename,
            user_id=str(current_user.id) # Pass user ID as string
        )
        logger.info(f"Conversion task {task.id} queued for {file.filename}")

        # TODO: Store initial file/conversion record in DB (Task 3.4)

        return {"message": "File uploaded successfully, conversion started.", "task_id": task.id}

    except Exception as e:
        logger.error(f"Error uploading file {file.filename} for user {current_user.id}: {e}", exc_info=True)
        # Clean up temp file if upload/queuing fails
        if temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process file upload.")
    finally:
        # Ensure the file pointer is closed
        await file.close()

# TODO: Add endpoint to check conversion status using task_id
# TODO: Add endpoint to download converted file 