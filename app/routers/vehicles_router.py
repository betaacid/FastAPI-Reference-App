from fastapi import APIRouter

from app.dependencies import DbSession, SwapiClientDep
from app.schemas.star_wars_vehicle_schema import (
    StarWarsVehicleCreate,
    StarWarsVehicleRead,
)
from app.services import vehicles_service

vehicles_router = APIRouter(prefix="/vehicles")


@vehicles_router.post("/", response_model=StarWarsVehicleRead)
async def create_vehicle(
    input_vehicle: StarWarsVehicleCreate,
    db: DbSession,
    swapi_client: SwapiClientDep,
) -> StarWarsVehicleRead:
    return await vehicles_service.add_new_vehicle(input_vehicle, db, swapi_client)


@vehicles_router.get("/{vehicle_id}", response_model=StarWarsVehicleRead)
async def read_vehicle(
    vehicle_id: int,
    db: DbSession,
) -> StarWarsVehicleRead:
    return await vehicles_service.get_vehicle_by_id(vehicle_id, db)
