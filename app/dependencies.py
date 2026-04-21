from fastapi import UploadFile, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.services.auth_service import get_user_by_email
import os

# ─── Image Validation ────────────────────────────────────────────────────────

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/avif"}
MAX_SIZE_MB = 10
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

async def validate_image(file: UploadFile) -> bytes:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported image type. Allowed: {', '.join(ALLOWED_TYPES)}")

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    if len(image_bytes) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=413, detail=f"File too large. Max size is {MAX_SIZE_MB}MB.")

    return image_bytes


# ─── Auth ─────────────────────────────────────────────────────────────────────
"""
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("JWT_ALGORITHM", "HS256")]
        )
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
        """