from fastapi import APIRouter, UploadFile, File, HTTPException
from server.queue.moderation_queue import moderation_queue, create_job


router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Soseska+ ok"}


@router.post("/moderate")
async def moderate_image_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()

    job = create_job(
        filename=file.filename or "unknown",
        image_bytes=image_bytes
    )

    await moderation_queue.put(job)

    try:
        result = await job.future
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))