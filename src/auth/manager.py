from typing import Optional

from fastapi import Depends
from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users import exceptions, models, schemas

from auth.models import User
from auth.utils import get_user_db, get_clearbit_data
from config import JWT_SECRET

SECRET = JWT_SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        clearbit_user_data = await get_clearbit_data(user_create.email)
        if clearbit_user_data:
            user_dict['first_name'] = clearbit_user_data.get('name').get('givenName')
            user_dict['last_name'] = clearbit_user_data.get('name').get('familyName')
            user_dict['country'] = clearbit_user_data.get('geo').get('country')
            user_dict['city'] = clearbit_user_data.get('geo').get('city')

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
