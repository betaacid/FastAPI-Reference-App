from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.star_wars_vehicle_schema import (
    StarWarsVehicleCreate,
    StarWarsVehicleRead,
)

from app.services.vehicles_service import add_new_vehicle, get_vehicle_by_id
from database import get_db_session

vehicles_router = APIRouter(prefix="/vehicles")


@vehicles_router.post("/", response_model=StarWarsVehicleRead)
async def create_vehicle(
    input_vehicle: StarWarsVehicleCreate,
    db: Session = Depends(get_db_session),
) -> StarWarsVehicleRead:
    return add_new_vehicle(input_vehicle, db)


@vehicles_router.get("/{vehicle_id}", response_model=StarWarsVehicleRead)
async def read_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db_session),
) -> StarWarsVehicleRead:
    return get_vehicle_by_id(vehicle_id, db)
