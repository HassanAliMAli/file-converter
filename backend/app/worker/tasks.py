import time
from app.core.celery_app import celery_app
import logging
from pathlib import Path
import os
import uuid

# --- Conversion Library Imports (Add as needed) ---
from PIL import Image # Import Pillow

# --- Database Imports ---
from app.db.session import SessionLocal # Import session factory
from app.models.conversion import Conversion, ConversionStatus
from app.models.file import File # Assuming File model needed for path
from sqlalchemy.orm import joinedload # To fetch related File object
from sqlalchemy import select, update

logger = logging.getLogger(__name__)

# Helper function to update conversion status in DB (runs within task context)
async def update_db_status(conversion_id: uuid.UUID, status: ConversionStatus, **kwargs):
    async with SessionLocal() as db:
        try:
            stmt = (
                update(Conversion)
                .where(Conversion.id == conversion_id)
                .values(status=status, **kwargs)
            )
            await db.execute(stmt)
            await db.commit()
            logger.info(f"Updated conversion {conversion_id} status to {status.value}")
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to update DB for conversion {conversion_id}: {e}", exc_info=True)

@celery_app.task(acks_late=True)
async def process_file_conversion(conversion_id_str: str):
    """Performs file conversion based on DB record, updates status, and cleans up."""

    conversion_id = uuid.UUID(conversion_id_str) # Convert string back to UUID
    logger.info(f"Starting conversion task for conversion_id: {conversion_id}")

    output_file_path = "" # Placeholder
    conversion = None
    input_path = None

    # --- Fetch Conversion Job Details from DB ---
    async with SessionLocal() as db:
        try:
            # Fetch Conversion and related File eagerly
            stmt = (
                select(Conversion)
                .options(joinedload(Conversion.original_file))
                .where(Conversion.id == conversion_id)
            )
            result = await db.execute(stmt)
            conversion = result.scalar_one_or_none()

            if not conversion or not conversion.original_file:
                logger.error(f"Conversion record {conversion_id} or associated file not found.")
                # Cannot proceed without job details
                return {"status": "error", "detail": "Conversion job or file not found"}

            # Mark as processing
            conversion.status = ConversionStatus.PROCESSING
            db.add(conversion)
            await db.commit()
            logger.info(f"Marked conversion {conversion_id} as PROCESSING")

            # Get details needed for conversion
            input_path = Path(conversion.original_file.storage_path)
            output_format = conversion.output_format
            original_filename = conversion.original_file.original_filename

        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to fetch/update conversion {conversion_id} from DB: {e}", exc_info=True)
            # We might retry later, or just fail
            # For now, just return error status
            return {"status": "error", "detail": f"Database error fetching job {conversion_id}"}

    # --- Perform Conversion ---
    try:
        logger.info(f"Performing conversion for '{original_filename}' to {output_format}")
        logger.info(f"Input file path: {input_path}")

        # Use configured directory for converted files
        output_dir = Path(settings.CONVERTED_DIR)
        output_dir.mkdir(exist_ok=True)
        # Use conversion ID to ensure unique output filename
        output_file_path = str(output_dir / f"{conversion_id}.{output_format}")

        # --- Select Conversion Library based on input/output formats --- 
        # Example using hypothetical conversion functions:
        try:
            input_content_type = conversion.original_file.content_type
            logger.info(f"Starting conversion: {input_content_type} -> {output_format}")

            if input_content_type.startswith("image/") and output_format in ["png", "jpg", "webp"]:
                # --- Pillow Image Conversion Example ---
                # NOTE: This is UNTESTED code. May require debugging and refinement.
                # It also doesn't handle all potential image modes or errors.
                logger.info(f"Attempting image conversion to {output_format} using Pillow...")
                try:
                    # Import inside try to avoid issues if Pillow isn't installed/needed
                    from PIL import Image, UnidentifiedImageError

                    img = Image.open(input_path)

                    # Handle different image modes for compatibility
                    current_mode = img.mode
                    logger.info(f"Opened image '{original_filename}' with mode: {current_mode}")

                    # Convert palettes to RGB/RGBA first
                    if current_mode in ('P', 'PA'):
                        logger.info(f"Converting image mode {current_mode} to RGBA")
                        img = img.convert('RGBA')
                        current_mode = img.mode # Update mode after conversion

                    # Ensure RGB for JPG output (strips transparency)
                    if output_format == 'jpg' and current_mode not in ('RGB', 'L'): # L is grayscale
                        logger.info(f"Converting image mode {current_mode} to RGB for JPG output")
                        img = img.convert('RGB')
                    # Preserve transparency for PNG/WEBP if present
                    elif output_format in ('png', 'webp') and current_mode == 'RGBA':
                         logger.info(f"Preserving RGBA mode for {output_format.upper()} output")
                    # Default conversion for other cases if needed (might not be necessary)
                    # elif current_mode not in ('RGB', 'RGBA', 'L'):
                    #     logger.warning(f"Unexpected image mode {current_mode}, attempting generic RGBA conversion.")
                    #     img = img.convert('RGBA')

                    # Pillow determines format from file extension for save,
                    # but we specify explicitly for clarity and potentially unsupported extensions
                    save_kwargs = {'format': output_format.upper()}
                    if output_format == 'jpg':
                        save_kwargs['quality'] = 85 # Example quality setting
                        save_kwargs['optimize'] = True
                    elif output_format == 'png':
                         save_kwargs['optimize'] = True
                    elif output_format == 'webp':
                        save_kwargs['quality'] = 85 # Example quality setting
                        # Add lossless=True or method=6 for different webp options if desired

                    img.save(output_file_path, **save_kwargs)
                    logger.info(f"Pillow conversion successful to {output_file_path}")

                except UnidentifiedImageError as img_err:
                    logger.error(f"Pillow could not identify image file: {img_err}", exc_info=True)
                    raise ValueError(f"Invalid or unsupported image file: {original_filename}")
                except (OSError, IOError) as io_err: # Catch file system related errors during open/save
                    logger.error(f"Pillow I/O error during conversion: {io_err}", exc_info=True)
                    raise ValueError(f"Error processing image file: {io_err}")
                except Exception as img_exc: # Catch other potential Pillow errors
                    logger.error(f"Pillow conversion failed unexpectedly: {img_exc}", exc_info=True)
                    raise ValueError(f"Image conversion failed: {img_exc}") # Raise specific error
                # --- End Pillow Example ---
            elif input_content_type == "application/pdf" and output_format == "txt":
                # from conversion_libs import pdf_converter
                # pdf_converter.to_text(str(input_path), output_file_path)
                logger.info("Simulating PDF to TXT conversion...")
                time.sleep(10) # Simulate PDF conversion time
            # Add more conditions for other supported conversions (audio, video, documents...)
            else:
                raise NotImplementedError(f"Conversion from {input_content_type} to {output_format} not supported.")

            # --- TODO: If storing results in cloud storage, upload output_file_path here --- 
            # Example: cloud_url = upload_to_s3(output_file_path)
            # Example: output_file_path = cloud_url # Update path to the cloud URL

            logger.info(f"Successfully converted to {output_file_path}")

        except Exception as conversion_error:
            logger.error(f"Actual conversion failed: {conversion_error}", exc_info=True)
            # Re-raise the error to be caught by the outer try/except
            raise conversion_error
        # --- End Conversion Logic ---

        logger.info(f"Conversion successful for {original_filename}. Output: {output_file_path}")

        # Update DB status to COMPLETED
        await update_db_status(
            conversion_id, ConversionStatus.COMPLETED, converted_file_path=output_file_path
        )

        return {"status": "success", "output_path": output_file_path}

    except Exception as e:
        error_message = f"Conversion failed for {original_filename}: {e}"
        logger.error(error_message, exc_info=True)

        # Update DB status to FAILED
        await update_db_status(
            conversion_id, ConversionStatus.FAILED, error_message=str(e)
        )

        raise # Reraise exception for Celery to mark task as failed

    finally:
        # --- Cleanup Input File ---
        # Cleanup only if input_path was successfully retrieved
        if input_path and input_path.exists():
            try:
                input_path.unlink()
                logger.info(f"Cleaned up temporary input file: {input_path}")
            except OSError as unlink_error:
                logger.error(f"Error cleaning up temporary file {input_path}: {unlink_error}") 