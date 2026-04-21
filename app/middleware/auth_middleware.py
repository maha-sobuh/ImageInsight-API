from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
import os

PROTECTED_PREFIXES = ["/v1/"]
PUBLIC_PATHS = ["/auth/login", "/docs", "/openapi.json", "/redoc"]


async def auth_middleware(request: Request, call_next):
    path = request.url.path

    if any(path.startswith(p) for p in PUBLIC_PATHS) or not any(path.startswith(p) for p in PROTECTED_PREFIXES):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Missing or invalid token."})

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("JWT_ALGORITHM", "HS256")]
        )
        email = payload.get("sub")
        if not email:
            return JSONResponse(status_code=401, content={"detail": "Invalid token."})
    except JWTError:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token."})

    return await call_next(request)