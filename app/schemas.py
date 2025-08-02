from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class UserProfileCreate(BaseModel):
    email: str
    full_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class UserProfileRead(UserProfileCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
