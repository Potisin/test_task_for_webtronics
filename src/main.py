import logging

from fastapi import FastAPI, Depends

from auth.base_config import current_user
from auth.models import User
from auth.router import router as auth_router
from posts.router import router as posts_router

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title='Webtronics App')

app.include_router(auth_router)
app.include_router(posts_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"
