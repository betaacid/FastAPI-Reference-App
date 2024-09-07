from fastapi import APIRouter, HTTPException

from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.services.characters_service import add_new_character

characters_router = APIRouter(prefix="/characters")


@characters_router.post("/", response_model=StarWarsCharacterRead)
def create_character(input_character: StarWarsCharacterCreate):
    return add_new_character(input_character)
