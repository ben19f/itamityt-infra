from sqlalchemy.orm import Session
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate


def get_items(db: Session, owner_id: int):

    return db.query(Item).filter(Item.owner_id == owner_id).all()


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()

    if not db_item:
        return None

    for key, value in item.model_dump().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def create_item(db: Session, item: ItemCreate, owner_id: int):

    db_item = Item(
        **item.model_dump(),
        owner_id=owner_id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item



def delete_item(db: Session, db_item: Item):
    db.delete(db_item)
    db.commit()
    return {"ok": True}