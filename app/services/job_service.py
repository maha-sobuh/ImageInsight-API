import uuid
import json
import asyncio
from typing import Callable
import redis.asyncio as aioredis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
JOB_TTL = 3600

redis_client = aioredis.from_url(REDIS_URL)


async def create_job(func: Callable, *args) -> str:
    job_id = str(uuid.uuid4())
    await redis_client.set(job_id, json.dumps({"status": "processing"}), ex=JOB_TTL)
    asyncio.create_task(_run_job(job_id, func, *args))
    return job_id


async def _run_job(job_id: str, func: Callable, *args):
    try:
        result = await func(*args)
        await redis_client.set(job_id, json.dumps({"status": "completed", "result": result}), ex=JOB_TTL)
    except Exception as e:
        await redis_client.set(job_id, json.dumps({"status": "failed", "error": "Something went wrong, please try again."}), ex=JOB_TTL)


async def get_job(job_id: str) -> dict | None:
    data = await redis_client.get(job_id)
    if not data:
        return None
    return json.loads(data)