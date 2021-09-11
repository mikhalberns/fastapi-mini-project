from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db_utils.database import get_db
from db_utils.schemas import Item, ShowItem
from repository import items

router = APIRouter(
    tags=["item"],
    prefix="/item"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item, db: Session = Depends(get_db)):
    return items.creat_item(item, db)


@router.get("/{id}", response_model=ShowItem)
def get_item(id: int, db: Session = Depends(get_db)):
    return items.get_item(id, db)


@router.get("/", response_model=List[ShowItem], tags=["item"])
def all_items(db: Session = Depends(get_db)):
    return items.all_items(db)
