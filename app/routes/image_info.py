from fastapi import APIRouter
from app.schemas.image_schema import ImageRequest
from app.services.image_analyzer import analyze_image
from app.services.storage_service import get_image , get_image_url
from fastapi.responses import Response


router = APIRouter()

@router.post("/v1/image-info")
async def image_info(request: ImageRequest):
    result = await analyze_image(request)
    return result

@router.get("/v1/images/url/{image_id}") ## not REST standared 
async def get_stored_image_url(image_id: str):
    url = get_image_url(image_id)
    return {"url": url}

@router.get("/v1/images/{image_id}")
async def get_stored_image(image_id: str):
    image_bytes = await get_image(image_id)
    return Response(content=image_bytes, media_type="image/jpeg")

