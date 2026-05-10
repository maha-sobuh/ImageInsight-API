import aioboto3
import boto3
import uuid
import os
from dotenv import load_dotenv


load_dotenv()

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
SESSION = aioboto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

async def save_image(image_bytes: bytes, file_type: str) -> str:
    extension = (file_type or "png").lower()
    filename = f"{str(uuid.uuid4())}.{extension}"

    async with SESSION.client("s3") as s3:
        await s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"images/{filename}",
            Body=image_bytes,
            ContentType=f"image/{extension}"
        )
    return filename

async def get_image(image_id: str) -> bytes:
    async with SESSION.client("s3") as s3:
        response = await s3.get_object(Bucket=BUCKET_NAME, Key=f"images/{image_id}")
        return await response["Body"].read()
    
def get_image_url(image_id: str):
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": f"images/{image_id}"},
    )
    return url
#_____________________________________________________________________________________________________

async def save_removed_bg_image(image_bytes: bytes) -> str:
    filename = f"{str(uuid.uuid4())}.png"
    async with SESSION.client("s3") as s3:
        await s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"removed-bg/{filename}",
            Body=image_bytes,
            ContentType="image/png"
        )
    return filename

def get_removed_bg_image_url(image_id: str) -> str:
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": f"removed-bg/{image_id}"},
    )
    return url

async def get_removed_bg_image(image_id: str) -> bytes:
    async with SESSION.client("s3") as s3:
        response = await s3.get_object(
            Bucket=BUCKET_NAME, 
            Key=f"removed-bg/{image_id}"
        )
        return await response["Body"].read()
    
#    __________________________________________________________________________________

async def save_generated_image(image_bytes: bytes) -> str:
    filename = f"{str(uuid.uuid4())}.png"
    async with SESSION.client("s3") as s3:
        await s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"generated-images/{filename}",
            Body=image_bytes,
            ContentType="image/png"
        )
    return filename

def get_generated_image_url(image_id: str) -> str:
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": f"generated-images/{image_id}"},
    )
    return url

async def get_generated_image(image_id: str) -> bytes:
    async with SESSION.client("s3") as s3:
        response = await s3.get_object(
            Bucket=BUCKET_NAME,
            Key=f"generated-images/{image_id}"
        )
        return await response["Body"].read()