from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
