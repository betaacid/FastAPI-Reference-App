import pytest
from app.domain.vehicles.vehicle_calculations import (
    calculate_vehicle_efficiency,
    convert_consumables_to_days,
)
from app.schemas.swapi_vehicle_schema import SwapiVehicle


def test_convert_consumables_to_days():
    assert convert_consumables_to_days("1 day") == 1
    assert convert_consumables_to_days("2 weeks") == 14
    assert convert_consumables_to_days("3 months") == 90
    assert convert_consumables_to_days("1 year") == 365


def test_calculate_vehicle_efficiency():
    vehicle = SwapiVehicle(
        name="Test Vehicle",
        model="Test Model",
        manufacturer="Test Manufacturer",
        cost_in_credits="10000",
        length="10",
        max_atmosphering_speed="1000",
        crew="2",
        passengers="4",
        cargo_capacity="1000",
        consumables="1 month",
        vehicle_class="Test Class",
        pilots=[],
    )
    efficiency = calculate_vehicle_efficiency(vehicle)

    # Calculate expected efficiency
    cargo_capacity = 1000
    crew = 2
    passengers = 4
    consumables_days = 30
    expected_efficiency = (cargo_capacity / (crew + passengers)) / consumables_days

    assert efficiency == expected_efficiency
