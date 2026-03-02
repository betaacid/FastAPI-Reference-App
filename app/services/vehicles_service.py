from fastapi import Depends
from app.clients.database.vehicles_database_client import VehiclesDatabaseClient
from app.clients.networking.swapi_networking_client import (
    get_vehicle_from_swapi,
    transform_swapi_vehicle_json_to_pydantic,
)
from app.schemas.star_wars_vehicle_schema import (
    StarWarsVehicleCreate,
    StarWarsVehicleRead,
)
from app.models.star_wars_vehicle_model import StarWarsVehicle
from app.domain.vehicles.vehicle_calculations import calculate_vehicle_efficiency


class VehiclesService:
    def __init__(self, db_client: VehiclesDatabaseClient = Depends(VehiclesDatabaseClient)):
        self.db_client = db_client

    def add_new_vehicle(
        self, input_vehicle: StarWarsVehicleCreate
    ) -> StarWarsVehicleRead:
        swapi_json = get_vehicle_from_swapi(input_vehicle.name)
        swapi_vehicle = transform_swapi_vehicle_json_to_pydantic(swapi_json)
        swapi_vehicle.efficiency = calculate_vehicle_efficiency(swapi_vehicle)
        new_vehicle: StarWarsVehicle = self.db_client.insert_new_vehicle(swapi_vehicle)

        return StarWarsVehicleRead.model_validate(new_vehicle)

    def get_vehicle_by_id(self, vehicle_id: int) -> StarWarsVehicleRead:
        vehicle = self.db_client.get_vehicle_by_id(vehicle_id)
        return StarWarsVehicleRead.model_validate(vehicle)
