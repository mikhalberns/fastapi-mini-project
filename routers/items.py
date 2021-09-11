from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from db_utils import models
from db_utils.database import get_db
from db_utils.schemas import Item, ShowItem

router = APIRouter()


@router.post("/item", status_code=status.HTTP_201_CREATED, tags=["item"])
def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = models.Item(name=item.name, size=item.size, user_id=1)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/item/{id}", response_model=ShowItem, tags=["item"])
def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    return item


@router.get("/item", response_model=List[ShowItem], tags=["item"])
def all_items(db: Session = Depends(get_db)):
    item = db.query(models.Item).all()
    return item
