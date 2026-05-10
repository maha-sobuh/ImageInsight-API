from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
from app.schemas.image_schema import GenerateImageRequest
from app.services.image_generator_service import generate_image, process_generate_image
from app.services.storage_service import save_generated_image, get_generated_image_url, get_generated_image
from app.services.job_service import create_job, get_job

router = APIRouter()

# ─── Sync ─────────────────────────────────────────────────────────────────────

@router.post("/v1/generate-image")
async def generate_image_endpoint(request: GenerateImageRequest):
    image_bytes = await generate_image(request)
    image_id = await save_generated_image(image_bytes)
    url = get_generated_image_url(image_id)
    return {
        "image_id": image_id,
        "url": url,
        "message": "Image generated successfully."
    }

@router.get("/v1/generate-image/{image_id}")
async def get_generated_image_endpoint(image_id: str):
    image_bytes = await get_generated_image(image_id)
    return Response(content=image_bytes, media_type="image/png")

# ─── Async ────────────────────────────────────────────────────────────────────

@router.post("/v1/async/generate-image")
async def generate_image_async_endpoint(request: GenerateImageRequest, req: Request):
    job_id = await create_job(process_generate_image, request)
    base_url = str(req.base_url).rstrip("/")
    return {
        "request_id": job_id,
        "status_url": f"{base_url}/v1/async/generate-image/{job_id}"
    }

@router.get("/v1/async/generate-image/{job_id}")
async def get_async_result_endpoint(job_id: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job["status"] == "processing":
        return {"status": "processing"}
    if job["status"] == "failed":
        return {"status": "failed", "error": "Something went wrong, please try again."}
    return {"status": "completed", **job["result"]}