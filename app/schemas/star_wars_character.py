from pydantic import BaseModel


class StarWarsCharacterBase(BaseModel):
    name: str
    rating: int


class StarWarsCharacterCreate(StarWarsCharacterBase):
    pass


class StarWarsCharacterRead(StarWarsCharacterBase):
    id: int
    height: str
    mass: str
