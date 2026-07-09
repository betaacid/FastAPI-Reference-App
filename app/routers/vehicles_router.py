from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_vehicles_service
from app.schemas.star_wars_vehicle_schema import (
    StarWarsVehicleCreate,
    StarWarsVehicleRead,
)
from app.services.vehicles_service import VehiclesService

vehicles_router = APIRouter(prefix="/vehicles")


@vehicles_router.post("/", response_model=StarWarsVehicleRead)
async def create_vehicle(
    input_vehicle: StarWarsVehicleCreate,
    service: Annotated[VehiclesService, Depends(get_vehicles_service)],
) -> StarWarsVehicleRead:
    return await service.add_new_vehicle(input_vehicle)


@vehicles_router.get("/{vehicle_id}", response_model=StarWarsVehicleRead)
async def read_vehicle(
    vehicle_id: int,
    service: Annotated[VehiclesService, Depends(get_vehicles_service)],
) -> StarWarsVehicleRead:
    return await service.get_vehicle_by_id(vehicle_id)
