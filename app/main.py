from fastapi import FastAPI
from app.routes import image_info
from app.routes import image_remove_background
from app.routes import auth
from app.routes import image_generator  

from app.db.database import create_tables
from app.middleware.auth_middleware import auth_middleware

app = FastAPI()

app.include_router(image_info.router)
app.include_router(image_remove_background.router)
app.include_router(auth.router)
app.include_router(image_generator.router)  
app.middleware("http")(auth_middleware)

@app.on_event("startup")
async def startup():
    await create_tables()