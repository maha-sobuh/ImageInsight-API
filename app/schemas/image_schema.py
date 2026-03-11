from pydantic import BaseModel , HttpUrl , Base64Str , model_validator
from typing import Optional 

class ImageRequest(BaseModel) : 
    base64 : Optional[Base64Str]=None 
    url : Optional[HttpUrl]=None 
    @model_validator(mode="after")
    def check_at_least_one(self):
        if not self.base64 and not self.url:
            raise ValueError("Provide either 'base64' or 'url'")
        return self

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