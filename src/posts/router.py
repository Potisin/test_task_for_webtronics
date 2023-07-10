from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from posts.models import Post, Like, Dislike
from posts.schemas import PostRead, PostCreate
from posts.utils import get_post_by_id, create_reaction, delete_reaction

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
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
    stmt = select(Post).order_by(desc(Post.created_at))
    result = await session.scalars(stmt)
    data = result.all()
    return data


@router.get("/{post_id}", response_model=PostRead)
async def get_post_by_id_router(post_id: int, session: AsyncSession = Depends(get_async_session)):
    post = await get_post_by_id(post_id, session)
    return post


@router.get("/my/")
async def get_own_posts(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    stmt = select(Post).filter_by(user_id=user.id).order_by(desc(Post.created_at))
    result = await session.scalars(stmt)
    return result.all()


@router.put("/{post_id}")
async def edit_post(post_id: int, text: str, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    stmt = update(Post).filter_by(id=post_id, user_id=user.id).values(text=text)
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post not found or not enough permissions")

    await session.commit()
    data = {'status': 'success'}
    return data


@router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    stmt = delete(Post).filter_by(id=post_id, user_id=user.id)
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post not found or not enough permissions")

    await session.commit()
    data = {'status': 'success'}
    return data


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
async def like_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    return await create_reaction(Like, post_id, user, session)


@router.delete("/{post_id}/like")
async def delete_like(post_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    return await delete_reaction(Like, post_id, user, session)


@router.post("/{post_id}/dislike", status_code=status.HTTP_201_CREATED)
async def dislike_post(post_id: int, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    return await create_reaction(Dislike, post_id, user, session)


@router.delete("/{post_id}/dislike")
async def delete_dislike(post_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    return await delete_reaction(Dislike, post_id, user, session)



