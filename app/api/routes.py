from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud import create_user, get_user_by_email
from app.db import get_session
from app.models import UserProfileCreate, UserProfileRead

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/users", response_model=UserProfileRead)
def create_user_profile(user: UserProfileCreate, session: Session = Depends(get_session)):
    existing_user = get_user_by_email(session, user.email)
    if existing_user:
        return existing_user
    return create_user(session, user)
