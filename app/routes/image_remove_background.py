from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from app.services.background_remover import remove_background
from app.services.storage_service import save_removed_bg_image, get_removed_bg_image_url,get_removed_bg_image
from app.dependencies import validate_image 
import asyncio
from app.db.models import User
router = APIRouter()

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