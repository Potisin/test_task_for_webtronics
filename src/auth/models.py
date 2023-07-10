from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user",
                                               cascade="save-update, delete, delete-orphan")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="user",
                                               cascade="save-update, delete, delete-orphan")
    dislikes: Mapped[List["Like"]] = relationship("Dislike", back_populates="user",
                                                  cascade="save-update, delete, delete-orphan")
