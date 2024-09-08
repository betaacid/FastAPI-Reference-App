from fastapi import FastAPI
from app.routers.characters_router import characters_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(characters_router)
