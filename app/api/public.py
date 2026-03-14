from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from db.crud_user import get_user_by_username
from db.crud_item import get_items_by_user_id
from schemas.item import Item  # схема для Item

router = APIRouter(prefix="/public", tags=["public"])

@router.get("/profile/{username}", response_model=list[Item])
def public_profile(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    items = get_items_by_user_id(db, user.id)
    return items
