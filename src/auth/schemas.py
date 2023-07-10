from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


class CustomBaseUserCreate(schemas.BaseUserCreate):
    password: Optional[str] = None

    class Config:
        orm_mode = True


class UserInput(CustomBaseUserCreate):
    password: str


class UserRead(CustomBaseUserCreate):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


class PostAuthor(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
