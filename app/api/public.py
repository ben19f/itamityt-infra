from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from db.crud_user import get_user_by_username
from db.crud_item import get_items_by_user_id
from schemas.user import User  # или отдельная схема
from schemas.item import Item  # схема длget_items_by_user_idя Item
from db.crud_user import get_last_users

router = APIRouter(prefix="/public", tags=["public"])

@router.get("/profile/{username}", response_model=list[Item])
def public_profile(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    items = get_items_by_user_id(db, user.id)
    return items

@router.get("/last-users")
def last_users(db: Session = Depends(get_db)):
    users = get_last_users(db, limit=3)  # берем 3 последних
    result = []
    for user in users:
        items = get_items_by_user_id(db, user.id)
        result.append({
            "username": user.username,
            "items": [{"name": i.name, "description": i.description} for i in items]
        })
    return result
