from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    is_active: bool = Field(default=True)