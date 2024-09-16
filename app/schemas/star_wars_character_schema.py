from pydantic import BaseModel, ConfigDict
from typing import Optional


class StarWarsCharacterBase(BaseModel):
    name: str


class StarWarsCharacterCreate(StarWarsCharacterBase):
    pass


class StarWarsCharacterRead(StarWarsCharacterBase):
    id: int
    height: Optional[str] = None
    mass: Optional[str] = None
    force: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
