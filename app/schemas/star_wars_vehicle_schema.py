from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class StarWarsVehicleBase(BaseModel):
    name: str
    model: str
    manufacturer: str

class StarWarsVehicleCreate(StarWarsVehicleBase):
    pass

class StarWarsVehicleRead(StarWarsVehicleBase):
    id: int
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    vehicle_class: str
    pilots: List[str]
    efficiency: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)