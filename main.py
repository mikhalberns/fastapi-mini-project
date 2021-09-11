from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from db_utils import models
from db_utils.database import engine, SessionLocal
from db_utils.hashing import Hash
from db_utils.schemas import User, Item, ShowUser, ShowItem

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/item", status_code=status.HTTP_201_CREATED, tags=["item"])
def create_item(item: Item, db: Session = Depends(get_db)):
    new_item = models.Item(name=item.name, size=item.size, user_id=100)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/item/{id}", response_model=ShowItem, tags=["item"])
def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found")
    return item


@app.get("/item", response_model=List[ShowItem], tags=["item"])
def all_items(db: Session = Depends(get_db)):
    item = db.query(models.Item).all()
    return item


@app.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["user"])
def update(id: int, user: User, db: Session = Depends(get_db)):
    edit_user = db.query(models.User).filter(models.User.id == id)
    if not edit_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    edit_user.update(user.dict())
    db.commit()
    return "updated"


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
def delete(id: int, db: Session = Depends(get_db)):
    delete_user = db.query(models.User).filter(models.User.id == id).first()
    if not delete_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    delete_user.delete(synchronize_session=False)
    db.commit()
    return {"message": "done"}


@app.post("/user", response_model=ShowUser, status_code=status.HTTP_201_CREATED, tags=["user"])
def create(user: User, db: Session = Depends(get_db)):
    new_user = models.User(email=user.email, is_active=user.is_active, password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user", response_model=List[ShowUser], tags=["user"])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/user/{id}", response_model=ShowUser, tags=["user"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    return user
