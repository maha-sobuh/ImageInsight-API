import io
import os
import sys
import asyncio
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision.transforms.functional import normalize
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

MODEL_INPUT_SIZE = [1024, 1024]
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = None

def _load_model():
    global model
    MODEL_PATH = os.getenv("RMBG_MODEL_PATH")
    if not MODEL_PATH:
        raise RuntimeError("RMBG_MODEL_PATH environment variable is not set.")
    if not os.path.isdir(MODEL_PATH):
        raise RuntimeError(f"RMBG_MODEL_PATH '{MODEL_PATH}' does not exist or is not a directory.")
    if MODEL_PATH not in sys.path:
        sys.path.insert(0, MODEL_PATH)

    from briarmbg import BriaRMBG  # type: ignore

    m = BriaRMBG.from_pretrained(MODEL_PATH)
    m.to(device)
    m.eval()
    model = m


def _preprocess(image: np.ndarray) -> torch.Tensor:
    if len(image.shape) < 3:
        image = image[:, :, np.newaxis]
    tensor = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1)
    tensor = F.interpolate(tensor.unsqueeze(0), size=MODEL_INPUT_SIZE, mode="bilinear")
    tensor = torch.divide(tensor, 255.0)
    tensor = normalize(tensor, [0.5, 0.5, 0.5], [1.0, 1.0, 1.0])
    return tensor


def _postprocess(result: torch.Tensor, orig_size: list) -> np.ndarray:
    result = torch.squeeze(F.interpolate(result, size=orig_size, mode="bilinear"), 0)
    ma, mi = torch.max(result), torch.min(result)
    result = (result - mi) / (ma - mi)
    return (result * 255).permute(1, 2, 0).cpu().data.numpy().astype(np.uint8).squeeze()


def _remove_background_sync(image_bytes: bytes) -> bytes:
    global model
    if model is None:
        _load_model()  # lazy load 

    pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    orig_size = [pil_image.size[1], pil_image.size[0]]
    np_image = np.array(pil_image)

    input_tensor = _preprocess(np_image).to(device)
    with torch.no_grad():
        result = model(input_tensor)

    mask = _postprocess(result[0][0], orig_size)
    pil_mask = Image.fromarray(mask)

    output = pil_image.copy().convert("RGBA")
    output.putalpha(pil_mask)

    output_buffer = io.BytesIO()
    output.save(output_buffer, format="PNG")
    return output_buffer.getvalue()


async def remove_background(image_bytes: bytes) -> bytes:
    return await asyncio.to_thread(_remove_background_sync, image_bytes)