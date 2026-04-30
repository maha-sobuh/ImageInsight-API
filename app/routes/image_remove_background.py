from fastapi import APIRouter, Depends, HTTPException ,Request
from fastapi.responses import Response
from app.services.background_remover import remove_background , process_remove_background
from app.services.storage_service import save_removed_bg_image, get_removed_bg_image_url, get_removed_bg_image
from app.services.job_service import create_job, get_job
from app.dependencies import validate_image
from app.db.models import User

router = APIRouter()


# ─── Sync ─────────────────────────────────────────────────────────────────────

@router.post("/v1/remove-background")
async def remove_background_endpoint(image_bytes: bytes = Depends(validate_image)):
    result_bytes = await remove_background(image_bytes)
    image_id = await save_removed_bg_image(result_bytes)
    url = get_removed_bg_image_url(image_id)
    return {
        "image_id": image_id,
        "url": url,
        "message": "Background removed successfully."
    }

@router.get("/v1/remove-background/{image_id}")
async def get_image_endpoint(image_id: str):
    image_bytes = await get_removed_bg_image(image_id)
    return Response(content=image_bytes, media_type="image/png")

# ─── Async ────────────────────────────────────────────────────────────────────

@router.post("/v1/async/remove-background")
async def remove_background_async_endpoint(
    request: Request,
    image_bytes: bytes = Depends(validate_image)
):
    job_id = await create_job(process_remove_background, image_bytes)
    base_url = str(request.base_url).rstrip("/")
    return {
        "request_id": job_id,
        "status_url": f"{base_url}/v1/async/remove-background/{job_id}"
    }

@router.get("/v1/async/remove-background/{job_id}")
async def get_async_result_endpoint(job_id: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job["status"] == "processing":
        return {"status": "processing"}
    if job["status"] == "failed":
        return {"status": "failed", "error": "Something went wrong, please try again."}
    return {"status": "completed", **job["result"]}