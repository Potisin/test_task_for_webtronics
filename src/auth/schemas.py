from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


class CustomBaseUserCreate(schemas.BaseUserCreate):
    username: str
    password: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(CustomBaseUserCreate):
    password: str


class UserRead(CustomBaseUserCreate):
    id: int


class PostAuthor(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
