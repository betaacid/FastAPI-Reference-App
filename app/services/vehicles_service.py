from app.clients.database.vehicles_database_client import VehiclesDatabaseClient
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


class VehiclesService:
    def __init__(self, db_client: VehiclesDatabaseClient, swapi_client: SwapiClient):
        self.db_client = db_client
        self.swapi_client = swapi_client

    async def add_new_vehicle(
        self, input_vehicle: StarWarsVehicleCreate
    ) -> StarWarsVehicleRead:
        swapi_json = await self.swapi_client.get_vehicle(input_vehicle.name)
        swapi_vehicle = transform_swapi_vehicle_json_to_pydantic(swapi_json)
        swapi_vehicle.efficiency = calculate_vehicle_efficiency(swapi_vehicle)
        new_vehicle = await self.db_client.insert_new_vehicle(swapi_vehicle)

        return StarWarsVehicleRead.model_validate(new_vehicle)

    async def get_vehicle_by_id(self, vehicle_id: int) -> StarWarsVehicleRead:
        vehicle = await self.db_client.get_vehicle_by_id(vehicle_id)
        if vehicle is None:
            raise VehicleNotFoundError(f"Vehicle {vehicle_id} not found")
        return StarWarsVehicleRead.model_validate(vehicle)
