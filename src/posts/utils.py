from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_async_session
from posts.models import Like, Dislike, Post

REACTION_CONFIG = {
    Like: {
        "count_field": "likes_count",
        "opposite_model": Dislike,
        "opposite_field": "dislikes_count"
    },
    Dislike: {
        "count_field": "dislikes_count",
        "opposite_model": Like,
        "opposite_field": "likes_count"
    }
}



async def get_post_by_id(post_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Post).filter_by(id=post_id).options(selectinload(Post.user))
    post = await session.scalar(stmt)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def create_reaction(reaction_model, post_id, user, session):
    post = await get_post_by_id(post_id, session)
    reaction_config = REACTION_CONFIG[reaction_model]
    stmt = select(reaction_model).filter_by(post_id=post_id, user_id=user.id)
    existing_reaction = await session.scalar(stmt)
    if existing_reaction or post.user_id == user.id:
        raise HTTPException(status_code=400,
                            detail="User already reacted or you are trying to react to your own post")
    stmt = delete(reaction_config["opposite_model"]).filter_by(post_id=post_id, user_id=user.id)
    result = await session.execute(stmt)
    if result.rowcount != 0:
        setattr(post, reaction_config["opposite_field"], getattr(post, reaction_config["opposite_field"]) - 1)
    reaction = reaction_model(post_id=post_id, user_id=user.id)
    session.add(reaction)
    setattr(post, reaction_config["count_field"], getattr(post, reaction_config["count_field"]) + 1)
    await session.commit()
    return {"detail": "Reaction added successfully."}


async def delete_reaction(reaction_model, post_id, user, session):
    post = await get_post_by_id(post_id, session)
    reaction_config = REACTION_CONFIG[reaction_model]
    stmt = delete(reaction_model).filter_by(post_id=post_id, user_id=user.id)
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Reaction not found or not enough permissions")
    setattr(post, reaction_config["count_field"], getattr(post, reaction_config["count_field"]) - 1)
    await session.commit()
    return {"detail": "Reaction deleted successfully."}