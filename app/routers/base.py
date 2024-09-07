from fastapi import APIRouter

base_router = APIRouter()


@base_router.get("/")
async def root():
    return {"message": "Welcome to the Star Wars API"}
