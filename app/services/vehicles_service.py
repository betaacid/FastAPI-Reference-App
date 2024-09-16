from app.clients.database.vehicles_database_client import (
    insert_new_vehicle,
    get_vehicle_by_id,
)
from app.clients.networking.swapi_networking_client import (
    get_vehicle_from_swapi,
    transform_swapi_vehicle_json_to_pydantic,
)

from app.schemas.star_wars_vehicle_schema import (
    StarWarsVehicleCreate,
    StarWarsVehicleRead,
)

from app.models.star_wars_vehicle_model import StarWarsVehicle
from sqlalchemy.orm import Session

from app.domain.vehicles.vehicle_calculations import calculate_vehicle_efficiency


def add_new_vehicle(
    input_vehicle: StarWarsVehicleCreate,
    db: Session,
) -> StarWarsVehicleRead:
    swapi_json = get_vehicle_from_swapi(input_vehicle.name)
    swapi_vehicle = transform_swapi_vehicle_json_to_pydantic(swapi_json)
    swapi_vehicle.efficiency = calculate_vehicle_efficiency(swapi_vehicle)
    new_vehicle: StarWarsVehicle = insert_new_vehicle(db, swapi_vehicle)

    return StarWarsVehicleRead.model_validate(new_vehicle)


def get_vehicle_by_id(vehicle_id: int, db: Session) -> StarWarsVehicleRead:
    vehicle = get_vehicle_by_id(db, vehicle_id)
    return StarWarsVehicleRead.model_validate(vehicle)
