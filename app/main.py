from fastapi import FastAPI
from app.routes import image_info
from app.routes import image_remove_background

app = FastAPI()

app.include_router(image_info.router)
app.include_router(image_remove_background.router)