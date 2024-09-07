from pydantic import BaseModel


class StarWarsCharacterBase(BaseModel):
    name: str
    rating: int


class StarWarsCharacterCreate(StarWarsCharacterBase):
    pass


from typing import Optional


class StarWarsCharacterRead(StarWarsCharacterBase):
    id: int
    height: Optional[str] = None
    mass: Optional[str] = None
