from app.schemas.swapi_vehicle_schema import SwapiVehicle


def convert_consumables_to_days(consumables: str) -> int:
    time_units = {
        "day": 1,
        "days": 1,
        "week": 7,
        "weeks": 7,
        "month": 30,
        "months": 30,
        "year": 365,
        "years": 365,
    }

    number, unit = consumables.split()
    return int(number) * time_units[unit]


def calculate_vehicle_efficiency(vehicle: SwapiVehicle) -> float:
    try:
        cargo_capacity = float(vehicle.cargo_capacity)
        crew = int(vehicle.crew)
        passengers = int(vehicle.passengers)
        consumables = vehicle.consumables

        consumables_days = convert_consumables_to_days(consumables)

        efficiency = (cargo_capacity / (crew + passengers)) / consumables_days
    except (ValueError, ZeroDivisionError):
        efficiency = 0.0

    return efficiency
