import logging

from fastapi import FastAPI

from auth.router import router as auth_router
from posts.router import router as posts_router

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title='Webtronics App')

app.include_router(auth_router)
app.include_router(posts_router)


@app.get("/")
async def root():
    return {"message": "Swagger: localhost:8000/docs"}
