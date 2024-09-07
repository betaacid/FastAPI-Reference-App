from fastapi import FastAPI
from app.routers.base import base_router
from app.routers.characters import characters_router

app = FastAPI()

app.include_router(base_router)
app.include_router(characters_router)
