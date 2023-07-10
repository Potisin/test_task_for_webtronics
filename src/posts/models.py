from datetime import datetime, timezone
from typing import List

from sqlalchemy import Integer, ForeignKey, TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['User'] = relationship('User', back_populates='posts')
    likes_count: Mapped[int] = mapped_column(default=0)
    dislikes_count: Mapped[int] = mapped_column(default=0)
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="post",
                                               cascade="save-update, delete, delete-orphan")
    dislikes: Mapped[List["Like"]] = relationship("Dislike", back_populates="post",
                                               cascade="save-update, delete, delete-orphan")



class Like(Base):
    __tablename__ = 'like'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped['Post'] = relationship('Post', back_populates='likes')
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['User'] = relationship('User', back_populates='likes')


class Dislike(Base):
    __tablename__ = 'dislike'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped['Post'] = relationship('Post', back_populates='dislikes')
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['User'] = relationship('User', back_populates='dislikes')
