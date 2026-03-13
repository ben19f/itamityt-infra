from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.item import Item, ItemCreate, ItemUpdate
from db.crud_item import (
    get_items,
    get_item,
    create_item,
    update_item,
    delete_item
)

from api.deps import get_current_user
from models.user import User

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[Item])
def read_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_items(db, current_user.id)


@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.post("/", response_model=Item)
def create_new_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_item(db, item, current_user.id)


@router.put("/{item_id}", response_model=Item)
def update_existing_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    updated = update_item(db, item_id, item)

    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated


@router.delete("/{item_id}")
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_item(db, item_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted"}