from sqlmodel import Session, select
from app.models import UserProfile
from app.schemas import UserProfileCreate
from uuid import UUID
from typing import List

def create_user(session: Session, user: UserProfileCreate) -> UserProfile:
    db_user = UserProfile(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(session: Session, email: str):
    return session.exec(select(UserProfile).where(UserProfile.email == email)).first()

def get_user_by_id(session: Session, user_id: UUID):
    return session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()

def get_all_users(session: Session) -> List[UserProfile]:
    return session.exec(select(UserProfile)).all()