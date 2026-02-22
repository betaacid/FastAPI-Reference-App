from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.star_wars_vehicle_model import StarWarsVehicle
from app.schemas.swapi_vehicle_schema import SwapiVehicle
from database import get_db_session


class VehiclesDatabaseClient:
    def __init__(self, db: Session = Depends(get_db_session)):
        self.db = db

    def insert_new_vehicle(self, swapi_vehicle: SwapiVehicle) -> StarWarsVehicle:
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
        )
        self.db.add(new_vehicle)
        self.db.flush()
        self.db.refresh(new_vehicle)
        self.db.commit()
        return new_vehicle

    def get_vehicle_by_id(self, vehicle_id: int) -> StarWarsVehicle:
        return self.db.query(StarWarsVehicle).filter(StarWarsVehicle.id == vehicle_id).first()
