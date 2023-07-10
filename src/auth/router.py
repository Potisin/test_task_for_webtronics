from fastapi import APIRouter

from auth.base_config import fastapi_users, auth_backend
from auth.schemas import UserRead, UserInput

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserInput),
    prefix="/auth",
    tags=["auth"],
)
