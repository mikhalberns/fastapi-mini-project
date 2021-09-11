from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db_utils.database import get_db
from db_utils.schemas import User, ShowUser
from repository import users

router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, user: User, db: Session = Depends(get_db)):
    return users.update(id, user, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    return users.delete(id, db)


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create(user: User, db: Session = Depends(get_db)):
    return users.create(user, db)


@router.get("/", response_model=List[ShowUser])
def all_users(db: Session = Depends(get_db)):
    return users.all_users(db)


@router.get("/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return users.get_user(id, db)
