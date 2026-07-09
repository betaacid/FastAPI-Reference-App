from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.star_wars_vehicle_model import StarWarsVehicle
from app.schemas.swapi_vehicle_schema import SwapiVehicle


async def insert_new_vehicle(
    db: AsyncSession, swapi_vehicle: SwapiVehicle
) -> StarWarsVehicle:
    new_vehicle = StarWarsVehicle(
        name=swapi_vehicle.name,
        model=swapi_vehicle.model,
        manufacturer=swapi_vehicle.manufacturer,
        cost_in_credits=swapi_vehicle.cost_in_credits,
        length=swapi_vehicle.length,
        max_atmosphering_speed=swapi_vehicle.max_atmosphering_speed,
        crew=swapi_vehicle.crew,
        passengers=swapi_vehicle.passengers,
        cargo_capacity=swapi_vehicle.cargo_capacity,
        consumables=swapi_vehicle.consumables,
        vehicle_class=swapi_vehicle.vehicle_class,
        efficiency=swapi_vehicle.efficiency,
    )
    db.add(new_vehicle)
    # flush assigns the id; the commit happens in get_db_session so one
    # request stays one transaction
    await db.flush()
    return new_vehicle


async def get_vehicle_by_id(
    db: AsyncSession, vehicle_id: int
) -> Optional[StarWarsVehicle]:
    return await db.get(StarWarsVehicle, vehicle_id)
