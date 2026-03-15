from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate, hashed_password: str):

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_last_users(db: Session, limit: int = 3):
    return db.query(User).order_by(User.id.desc()).limit(limit).all()
