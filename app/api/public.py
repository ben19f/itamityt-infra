from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.crud_user import get_user_by_username, get_last_users
from db.crud_item import get_items_by_user

from schemas.item import Item

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/profile/{username}", response_model=list[Item])
def public_profile(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    items = get_items_by_user(db, user.id)

    return items


@router.get("/last-users")
def last_users(db: Session = Depends(get_db)):
    users = get_last_users(db, limit=3)

    result = []

    for user in users:
        items = get_items_by_user(db, user.id)

        result.append({
            "username": user.username,
            "items": [
                {
                    "name": i.name,
                    "link_id": i.link_id
                }
                for i in items
            ]
        })

    return result
