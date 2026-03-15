# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session
#
# from db.session import get_db
# from schemas.item import Item, ItemCreate, ItemUpdate
# from db.crud_item import get_items, get_item, create_item, update_item, delete_item
# from api.deps import get_current_user
# from models.user import User
#
# router = APIRouter(prefix="/items", tags=["items"])
#
#
# @router.get("/", response_model=list[Item])
# def read_items(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return get_items(db, current_user.id)
#
#
# @router.get("/{item_id}", response_model=Item)
# def read_item(
#     item_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     item = get_item(db, item_id, current_user.id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item
#
#
# @router.post("/", response_model=Item)
# def create_new_item(
#     item: ItemCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return create_item(db, item, current_user.id)
#
#
# @router.put("/{item_id}", response_model=Item)
# def update_existing_item(
#     item_id: int,
#     item: ItemUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     db_item = get_item(db, item_id, current_user.id)
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return update_item(db, db_item, item)
#
#
# @router.delete("/{item_id}")
# def delete_existing_item(
#     item_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     db_item = get_item(db, item_id, current_user.id)
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return delete_item(db, db_item)
#
#
# @app.get("/items/", response_model=List[Item])
# async def read_items(db: AsyncSession = Depends(get_db)):
#     items = await get_all_items(db)
#     return [Item(
#         id=item.id,
#         name=item.name,
#         description=item.description,
#         link_id=item.link_id
#     ) for item in items]
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.deps import get_db
from db.crud_item import create_item, get_all_items, get_items_by_user, delete_item

from schemas.item import ItemCreate, Item

# router = APIRouter()
router = APIRouter(prefix="/items", tags=["items"])


@router.get("/items/", response_model=list[Item])
async def read_items(db: AsyncSession = Depends(get_db)):
    items = await get_all_items(db)
    return items

@router.post("/items/", response_model=Item)
async def add_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    new_item = await create_item(db, item.name, item.description)
    return new_item

@router.get("/profile/{user_id}", response_model=list[Item])
async def read_user_items(user_id: int, db: AsyncSession = Depends(get_db)):
    items = await get_items_by_user(db, user_id)
    return items

@router.delete("/items/{item_id}")
async def remove_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
