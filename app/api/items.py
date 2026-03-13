from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.item import ItemCreate
from app.db.deps import get_db
from app.models.item import Item

router = APIRouter(prefix="/items")

@router.post("/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    db_item = Item(name=item.name)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item