import asyncio
import uuid
from passlib.context import CryptContext
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import engine
from app.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed():
    async with AsyncSession(engine) as session:
        users = [
            User(
                id=str(uuid.uuid4()),
                email="maha@gmail.com",
                password=pwd_context.hash("12345678"),
                is_active=True
            ),
            User(
                id=str(uuid.uuid4()),
                email="hasan@gmail.com",
                password=pwd_context.hash("password123"),
                is_active=True
            ),
        ]
        for user in users:
            session.add(user)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())