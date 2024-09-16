from app.schemas.swapi_vehicle_schema import SwapiVehicle


def convert_consumables_to_days(consumables: str) -> int:
    """
    Converts the value of consumables to days.

    :param consumables: String representing the consumables time (e.g., "2 months")
    :return: Number of days
    """
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
    """
    Calculates the efficiency of a vehicle based on its attributes.

    :param vehicle: Instance of SwapiVehicle
    :return: Calculated efficiency of the vehicle
    """
    try:
        cargo_capacity = float(vehicle.cargo_capacity)
        crew = int(vehicle.crew)
        passengers = int(vehicle.passengers)
        consumables = vehicle.consumables

        # Convert consumables to days
        consumables_days = convert_consumables_to_days(consumables)

        # Calculate efficiency as a function of cargo capacity, crew, passengers, and consumables
        efficiency = (cargo_capacity / (crew + passengers)) / consumables_days
    except (ValueError, ZeroDivisionError):
        efficiency = 0.0

    return efficiency
