from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services.auth_service import login

router = APIRouter()

@router.post("/auth/login", response_model=TokenResponse)
async def login_endpoint(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await login(request.email, request.password, db)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    return TokenResponse(access_token=token)