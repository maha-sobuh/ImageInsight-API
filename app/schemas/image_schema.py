from pydantic import BaseModel, HttpUrl, model_validator
from typing import Optional
from PIL import Image
from io import BytesIO
import httpx
import base64

class ImageRequest(BaseModel) : 
    base64 : Optional[str]=None 
    url : Optional[HttpUrl]=None 

    @model_validator(mode="after")
    def check_at_least_one(self):
        if not self.base64 and not self.url:
            raise ValueError("Provide either 'base64' or 'url'")
        return self   
    async def load_image(self): 
        if self.base64:
            base64_str = self.base64
            base64_str += "=" * (4 - len(base64_str) % 4)
            image_bytes =  base64.b64decode(base64_str)
        else : 
            async with httpx.AsyncClient() as client:
                response = await client.get(str(self.url)) #returns response object 
                image_bytes = response.content
        return Image.open(BytesIO(image_bytes)),image_bytes

class ColorHistogram(BaseModel):
    red:list[int]
    green:list[int]
    blue:list[int]

class InfoResponse(BaseModel): 
    file_type:str 
    file_size:int
    width:int
    height:int 
    pixel_count:int 
    aspect_ratio:str
    alpha_channel:bool 
    histogram : ColorHistogram
    description : str="" 
    image_id: str = ""