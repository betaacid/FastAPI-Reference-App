from fastapi import FastAPI
from app.routers.base_router import base_router
from app.routers.characters_router import characters_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(base_router)
app.include_router(characters_router)
