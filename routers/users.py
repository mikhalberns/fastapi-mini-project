from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from db_utils import models
from db_utils.database import get_db
from db_utils.schemas import User, ShowUser

router = APIRouter()


@router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["user"])
def update(id: int, user: User, db: Session = Depends(get_db)):
    edit_user = db.query(models.User).filter(models.User.id == id)
    if not edit_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    edit_user.update(user.dict())
    db.commit()
    return "updated"


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
def delete(id: int, db: Session = Depends(get_db)):
    delete_user = db.query(models.User).filter(models.User.id == id).first()
    if not delete_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    delete_user.delete(synchronize_session=False)
    db.commit()
    return {"message": "done"}


@router.post("/user", response_model=ShowUser, status_code=status.HTTP_201_CREATED, tags=["user"])
def create(user: User, db: Session = Depends(get_db)):
    new_user = models.User(email=user.email, is_active=user.is_active, password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user", response_model=List[ShowUser], tags=["user"])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/user/{id}", response_model=ShowUser, tags=["user"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    return user
