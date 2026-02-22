from pydantic import BaseModel
from typing import Optional


class SwapiVehicle(BaseModel):
    name: str
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
