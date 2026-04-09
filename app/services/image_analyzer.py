from app.schemas.image_schema import ImageRequest , InfoResponse , ColorHistogram 
from app.services.storage_service import save_image , get_image_url
from app.services.llm_service import generate_description

import httpx
import base64
from io import BytesIO
from math import gcd
from PIL import Image
import asyncio

def get_aspect_ratio(width: int, height: int) -> str:
    ratios = [
        (1, 1),
        (4, 3),
        (3, 4),
        (3, 2),
        (2, 3),
        (16, 9),
        (9, 16),
        (21, 9),
        (9, 21),
    ]
    for w, h in ratios:
        if abs((width / height) - (w / h)) < 0.05:
            return f"{w}:{h}"
        
    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"

def get_histogram(img: Image.Image) -> ColorHistogram:
    rgb_img = img.convert("RGB")
    histogram = rgb_img.histogram()
    return ColorHistogram(
        red=histogram[0:256],
        green=histogram[256:512],
        blue=histogram[512:768]
    )
    
async def analyze_image(request:ImageRequest)->InfoResponse : 
    img,image_bytes=await request.load_image() 

   # image_id = await save_image(image_bytes, img.format) 
    
    info = {
        "file_type":img.format,
        "file_size":len(image_bytes),
        "width":img.width ,  
        "height":img.height ,
        "pixel_count":img.width*img.height ,
        "aspect_ratio":get_aspect_ratio(img.width,img.height),
        "alpha_channel":img.mode in ("RGBA", "LA", "PA")
    }

    """ image_id = await save_image(image_bytes, img.format)
    image_url = get_image_url(image_id)
    description = await generate_description(info, image_url)"""

    image_id, description = await asyncio.gather(
        save_image(image_bytes, img.format),
        generate_description(info,image_bytes)
    )
    histogram=get_histogram(img)
    return InfoResponse(
        **info , 
        histogram=histogram , 
        description=description , 
        image_id=image_id
    )