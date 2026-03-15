# from sqlalchemy.orm import Session
# from models.item import Item
# from schemas.item import ItemCreate, ItemUpdate
#
#
# # Получить все элементы конкретного пользователя
# def get_items(db: Session, owner_id: int):
#     return db.query(Item).filter(Item.owner_id == owner_id).all()
#
#
#
#
#
# # Получить конкретный элемент по id и владельцу
# def get_item(db: Session, item_id: int, owner_id: int):
#     return db.query(Item).filter(Item.id == item_id, Item.owner_id == owner_id).first()
#
#
# # Создать новый элемент для конкретного пользователя
# def create_item(db: Session, item: ItemCreate, owner_id: int):
#     db_item = Item(**item.model_dump(), owner_id=owner_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
#
#
# # Обновить существующий элемент
# def update_item(db: Session, db_item: Item, item_update: ItemUpdate):
#     for key, value in item_update.model_dump().items():
#         setattr(db_item, key, value)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
#
#
# # Удалить элемент
# def delete_item(db: Session, db_item: Item):
#     db.delete(db_item)
#     db.commit()
#     return {"ok": True}
#
#
# # crud_item.py
# def get_items_by_user_id(db: Session, user_id: int):
#     return db.query(Item).filter(Item.owner_id == user_id).all()


import string
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.item import Item

def generate_link_id(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

async def create_item(db: AsyncSession, name: str, description: str, owner_user_id: int = None):
    # Генерация уникального link_id
    while True:
        link_id = generate_link_id()
        existing = await db.execute(select(Item).filter_by(link_id=link_id))
        if not existing.scalar():
            break

    db_item = Item(
        name=name,
        description=description,
        link_id=link_id,
        owner_user_id=owner_user_id
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_all_items(db: AsyncSession):
    result = await db.execute(select(Item))
    return result.scalars().all()

async def get_items_by_user(db: AsyncSession, owner_user_id: int):
    result = await db.execute(select(Item).filter_by(owner_user_id=owner_user_id))
    return result.scalars().all()

async def get_item_by_link_id(db: AsyncSession, link_id: str):
    result = await db.execute(select(Item).filter_by(link_id=link_id))
    return result.scalar()

async def delete_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(Item).filter_by(id=item_id))
    item = result.scalar()
    if item:
        await db.delete(item)
        await db.commit()
    return item
