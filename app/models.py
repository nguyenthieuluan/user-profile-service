from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserProfile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=100, unique=True)
    full_name: str = Field(max_length=100)
    avatar_url: Optional[str] = Field(default=None, max_length=255)
    bio: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Input model when creating user profile
class UserProfileCreate(BaseModel):
    name: str
    email: str

# Output model when returning user profile data
class UserProfileRead(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True