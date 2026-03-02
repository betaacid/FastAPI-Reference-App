from pydantic import BaseModel, ConfigDict
from typing import Optional


class StarWarsVehicleBase(BaseModel):
    name: str


class StarWarsVehicleCreate(StarWarsVehicleBase):
    pass


class StarWarsVehicleRead(StarWarsVehicleBase):
    id: int
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    cost_in_credits: Optional[str] = None
    length: Optional[str] = None
    max_atmosphering_speed: Optional[str] = None
    crew: Optional[str] = None
    passengers: Optional[str] = None
    cargo_capacity: Optional[str] = None
    consumables: Optional[str] = None
    vehicle_class: Optional[str] = None
    efficiency: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
