from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db_utils import models
from db_utils.database import get_db
from db_utils.hashing import Hash
from db_utils.schemas import Login


def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credentials")
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid password")
    return user
