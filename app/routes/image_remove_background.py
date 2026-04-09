# app/routes/image_remove_background.py
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import Response
from app.services.background_remover import remove_background
from app.dependencies import validate_image

router = APIRouter()

@router.post("/v1/remove-background")
async def remove_background_endpoint(image_bytes: bytes = Depends(validate_image)):
    result_bytes = await remove_background(image_bytes)
    return Response(content=result_bytes, media_type="image/png")