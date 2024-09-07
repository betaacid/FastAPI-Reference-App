from fastapi import APIRouter, HTTPException

from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)

characters_router = APIRouter(prefix="/characters")

characters = []


@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(character: StarWarsCharacterCreate):
    new_character = StarWarsCharacterRead(
        id=1,
        name=character.name,
        rating=character.rating,
        height="123",
        mass="456",
    )
    return new_character


@characters_router.get("/{character_id}")
async def get_character(character_id: int):
    if character_id < 0 or character_id >= len(characters):
        raise HTTPException(status_code=404, detail="Character not found")
    return characters[character_id]
