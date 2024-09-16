from app.schemas.swapi_vehicle_schema import SwapiVehicle


def convert_consumables_to_days(consumables: str) -> int:
    """
    Converte o valor de consumables para dias.

    :param consumables: String representando o tempo de consumíveis (ex: "2 months")
    :return: Número de dias
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
    Calcula a eficiência de um veículo com base em seus atributos.

    :param vehicle: Instância de StarWarsVehicle
    :return: Eficiência calculada do veículo
    """
    try:
        cargo_capacity = float(vehicle.cargo_capacity)
        crew = int(vehicle.crew)
        passengers = int(vehicle.passengers)
        consumables = vehicle.consumables

        # Converter consumables para dias
        consumables_days = convert_consumables_to_days(consumables)

        # Calcular a eficiência como uma função de capacidade de carga, tripulação, passageiros e consumíveis
        efficiency = (cargo_capacity / (crew + passengers)) / consumables_days
    except (ValueError, ZeroDivisionError):
        efficiency = 0.0

    return efficiency
