import asyncio
import io
import torch
from diffusers import LCMScheduler, AutoPipelineForText2Image
from app.schemas.image_schema import GenerateImageRequest
from app.services.storage_service import save_generated_image, get_generated_image_url
from app.services import llm_service

_pipe = None

def _load_pipeline():
    global _pipe
    if _pipe is None:
        _pipe = AutoPipelineForText2Image.from_pretrained(
            "lykon/dreamshaper-7",
            torch_dtype=torch.float32,
        )
        _pipe.scheduler = LCMScheduler.from_config(_pipe.scheduler.config)
        _pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
        _pipe.to("gpu")
        _pipe.enable_attention_slicing()
    return _pipe

async def _enhance_prompt(prompt: str) -> str:
    if len(prompt.split()) <= 4:
        expanded =await llm_service.expand_image_prompt(prompt)
        print(f"Enhanced prompt: {expanded}") 
        return expanded
    return f"{prompt}, high quality, detailed, sharp focus"

async def generate_image(request: GenerateImageRequest) -> bytes:
    #enhanced_prompt = await _enhance_prompt(request.prompt)

    def run():
        pipe = _load_pipeline()
        image = pipe(
            request.prompt,
            negative_prompt="blurry, low quality, distorted, watermark",
            num_inference_steps=request.steps,
            guidance_scale=1.0,
            width=request.width,
            height=request.height,
        ).images[0]
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        return buf.read()

    return await asyncio.to_thread(run)

async def process_generate_image(request: GenerateImageRequest) -> dict:
    image_bytes = await generate_image(request)
    image_id = await save_generated_image(image_bytes)
    url = get_generated_image_url(image_id)
    return {
        "image_id": image_id,
        "url": url,
        "message": "Image generated successfully."
    }