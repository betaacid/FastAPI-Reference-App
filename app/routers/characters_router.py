from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.star_wars_character_schema import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.services.characters_service import add_new_character
from database import get_db_session

characters_router = APIRouter(prefix="/characters")


@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate,
    db: Session = Depends(get_db_session),
) -> StarWarsCharacterRead:
    return add_new_character(input_character, db)
