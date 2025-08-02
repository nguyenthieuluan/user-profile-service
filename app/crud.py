from sqlmodel import Session, select
from app.models import UserProfile
from app.schemas import UserProfileCreate

def create_user(session: Session, user: UserProfileCreate) -> UserProfile:
    db_user = UserProfile(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(session: Session, email: str):
    return session.exec(select(UserProfile).where(UserProfile.email == email)).first()