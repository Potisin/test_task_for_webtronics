from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from posts.models import Post
from posts.schemas import PostRead, PostCreate

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.post("/", status_code=201)
async def create_post(new_post: PostCreate, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    post_data = new_post.dict()
    new_post = Post(user_id=user.id, **post_data)
    session.add(new_post)
    await session.flush()
    await session.refresh(new_post)
    await session.commit()
    return new_post


@router.get("/")
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    query = select(Post).order_by(desc(Post.created_at))
    result = await session.scalars(query)
    data = result.all()
    return data


@router.get("/{post_id}", response_model=PostRead)
async def get_post_by_id(post_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == post_id).options(selectinload(Post.user))
    post = await session.scalar(query)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/my/")
async def get_own_posts(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    i = user.id
    query = select(Post).where(Post.user_id == user.id).order_by(desc(Post.created_at))
    result = await session.scalars(query)
    return result.all()


@router.put("/{post_id}")
async def edit_post(post_id: int, text: str, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    query = update(Post).where(Post.id == post_id, Post.user_id == user.id).values(text=text)
    result = await session.execute(query)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post not found or not enough permissions")

    await session.commit()
    data = {'status': 'success'}
    return data


@router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    query = delete(Post).where(Post.id == post_id, Post.user_id == user.id)
    result = await session.execute(query)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post not found or not enough permissions")

    await session.commit()
    data = {'status': 'success'}
    return data
