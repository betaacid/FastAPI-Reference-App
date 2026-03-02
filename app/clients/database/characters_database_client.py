from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.star_wars_character_model import StarWarsCharacter
from app.schemas.swapi_character_schema import SwapiCharacter
from database import get_db_session


class CharactersDatabaseClient:
    def __init__(self, db: Session = Depends(get_db_session)):
        self.db = db

    def insert_new_character(self, swapi_character: SwapiCharacter) -> StarWarsCharacter:
        new_character = StarWarsCharacter(
            name=swapi_character.name,
            height=swapi_character.height,
            mass=swapi_character.mass,
        )
        self.db.add(new_character)
        self.db.flush()
        self.db.refresh(new_character)
        self.db.commit()
        return new_character
