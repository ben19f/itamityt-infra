
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.deps import get_db
from db.crud_item import create_item, get_all_items, get_items_by_user, delete_item

from schemas.item import ItemCreate, Item
from models.user import User

from core.security import get_current_user  # если есть функция для current_user

# router = APIRouter()
router = APIRouter(prefix="/items", tags=["items"])



@router.get("/", response_model=list[Item])
async def read_items(db: AsyncSession = Depends(get_db)):
    items = await get_all_items(db)
    return items



@router.post("/items/", response_model=Item)
async def add_item(item: ItemCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_item = await create_item(
        db,
        item.name,
        item.description,
        owner_user_id=current_user.id  # <-- вот тут
    )
    return new_item


@router.get("/profile/{user_id}", response_model=list[Item])
async def read_user_items(user_id: int, db: AsyncSession = Depends(get_db)):
    items = await get_items_by_user(db, user_id)
    return items

@router.delete("/{item_id}")
async def remove_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
