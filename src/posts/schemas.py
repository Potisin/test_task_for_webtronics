from datetime import datetime

from pydantic import BaseModel

from auth.schemas import PostAuthor


class PostCreate(BaseModel):
    text: str

    class Config:
        orm_mode = True


class PostRead(PostCreate):
    id: int
    created_at: datetime
    likes_count: int
    dislikes_count: int
    user: PostAuthor
