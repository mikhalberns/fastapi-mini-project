from fastapi import FastAPI

from db_utils import models
from db_utils.database import engine
from routers import items, users, login

app = FastAPI()

app.include_router(login.router)
app.include_router(users.router)
app.include_router(items.router)

models.Base.metadata.create_all(bind=engine)
