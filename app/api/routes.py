from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from typing import List

from app.crud import create_user, get_user_by_email, get_user_by_id, get_all_users
from app.db import get_session
from app.schemas import UserProfileCreate, UserProfileRead

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/users", response_model=List[UserProfileRead])
def get_users(session: Session = Depends(get_session)):
    return get_all_users(session)

@router.get("/users/{user_id}", response_model=UserProfileRead)
def get_user(user_id: UUID, session: Session = Depends(get_session)):
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserProfileRead)
def create_user_profile(user: UserProfileCreate, session: Session = Depends(get_session)):
    existing_user = get_user_by_email(session, user.email)
    if existing_user:
        return existing_user
    return create_user(session, user)
