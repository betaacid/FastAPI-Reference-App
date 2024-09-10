from pydantic import BaseModel
from typing import List, Optional


class SwapiCharacter(BaseModel):
    name: str
    height: Optional[str]
    mass: Optional[str]
