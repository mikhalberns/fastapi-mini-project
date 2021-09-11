from typing import List

from pydantic import BaseModel


class User(BaseModel):
    email: str
    is_active: bool
    password: str


class Item(BaseModel):
    name: str
    size: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    email: str
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class ShowItem(BaseModel):
    name: str
    size: str
    owner: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str
