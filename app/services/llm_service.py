from openai import AsyncOpenAI
import base64
import os
from PIL import Image
from io import BytesIO

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """You are an image analysis expert.
You will receive image metadata and the image itself.
Write a single natural paragraph (2-3 sentences) that includes:
- What you see in the image
- The mood and colors
- One technical observation (dimensions, aspect ratio, or file type) if relevant
No bullet points, no headers, no markdown. Be concise and professional.
"""

def compress_image(image_bytes: bytes, max_size: int = 512) -> bytes:
    img = Image.open(BytesIO(image_bytes))
    img.thumbnail((max_size, max_size))
    if img.mode in ("RGBA", "LA", "PA"):  # convert if has alpha channel
        img = img.convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=70)
    return buffer.getvalue()

async def generate_description(image_info: dict, image_bytes: bytes) -> str:
    compressed = compress_image(image_bytes)  # compress before sending
    mime_type = "image/jpeg"
    image_b64 = base64.b64encode(compressed).decode("utf-8")

    response = await client.chat.completions.create(
        model="meta-llama/llama-3.2-11b-vision-instruct",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": f"Image metadata:\n{image_info}"},
                {"type": "image_url", "image_url": {
                    "url": f"data:{mime_type};base64,{image_b64}"
                }}
            ]}
        ]
    )
    return response.choices[0].message.content