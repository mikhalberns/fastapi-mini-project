from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db_utils import models
from db_utils.database import get_db
from db_utils.schemas import Item


def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = models.Item(name=item.name, size=item.size, user_id=1)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    return item


def all_items(db: Session = Depends(get_db)):
    item = db.query(models.Item).all()
    return item
