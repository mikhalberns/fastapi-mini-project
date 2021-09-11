from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db_utils.database import get_db
from db_utils.schemas import Login
from repository.login import login

router = APIRouter(
    tags=["login"]
)


@router.post("/login")
def login_user(request: Login, db: Session = Depends(get_db)):
    return login(request, db)
