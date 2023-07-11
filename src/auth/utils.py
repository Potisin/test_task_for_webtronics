import httpx
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from config import CLEARBIT_KEY
from database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_clearbit_data(email: EmailStr):
    url = f"https://person.clearbit.com/v1/people/email/{email}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=(CLEARBIT_KEY, ''))

    if response.status_code == 200:
        return response.json()
