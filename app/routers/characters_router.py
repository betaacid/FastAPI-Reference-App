from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.star_wars_character import (
    StarWarsCharacterCreate,
    StarWarsCharacterRead,
)
from app.services.characters_service import add_new_character
from database import get_db_session
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

characters_router = APIRouter(prefix="/characters")


@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate,
    db: Session = Depends(get_db_session),
) -> StarWarsCharacterRead:
    try:
        return add_new_character(input_character, db)
    except RequestException:
        raise HTTPException(
            status_code=503,
            detail="External service unavailable. Please try again later.",
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="Internal server error. Please try again later."
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Character not found: {e}")
