from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate


# Получить все элементы конкретного пользователя
def get_items(db: Session, owner_id: int):
    return db.query(Item).filter(Item.owner_id == owner_id).all()





# Получить конкретный элемент по id и владельцу
def get_item(db: Session, item_id: int, owner_id: int):
    return db.query(Item).filter(Item.id == item_id, Item.owner_id == owner_id).first()


# Создать новый элемент для конкретного пользователя
def create_item(db: Session, item: ItemCreate, owner_id: int):
    db_item = Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Обновить существующий элемент
def update_item(db: Session, db_item: Item, item_update: ItemUpdate):
    for key, value in item_update.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


# Удалить элемент
def delete_item(db: Session, db_item: Item):
    db.delete(db_item)
    db.commit()
    return {"ok": True}

