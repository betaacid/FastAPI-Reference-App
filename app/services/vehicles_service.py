from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.database import vehicles_database_client
from app.clients.networking.swapi_networking_client import (
    SwapiClient,
    transform_swapi_vehicle_json_to_pydantic,
)
from app.domain.vehicles.vehicle_calculations import calculate_vehicle_efficiency
from app.errors.custom_exceptions import VehicleNotFoundError
from app.schemas.star_wars_vehicle_schema import (
    StarWarsVehicleCreate,
    StarWarsVehicleRead,
)


async def add_new_vehicle(
    input_vehicle: StarWarsVehicleCreate,
    db: AsyncSession,
    swapi_client: SwapiClient,
) -> StarWarsVehicleRead:
    swapi_json = await swapi_client.get_vehicle(input_vehicle.name)
    swapi_vehicle = transform_swapi_vehicle_json_to_pydantic(swapi_json)
    swapi_vehicle.efficiency = calculate_vehicle_efficiency(swapi_vehicle)
    new_vehicle = await vehicles_database_client.insert_new_vehicle(db, swapi_vehicle)

    return StarWarsVehicleRead.model_validate(new_vehicle)


async def get_vehicle_by_id(vehicle_id: int, db: AsyncSession) -> StarWarsVehicleRead:
    vehicle = await vehicles_database_client.get_vehicle_by_id(db, vehicle_id)
    if vehicle is None:
        raise VehicleNotFoundError(f"Vehicle {vehicle_id} not found")
    return StarWarsVehicleRead.model_validate(vehicle)
