class SwapiCharacterError(Exception):
    """Exception raised when an error occurs while fetching or parsing a SWAPI character."""

    pass


class CharacterNotFoundError(SwapiCharacterError):
    """Exception raised when a character is not found in SWAPI."""

    pass


class SwapiVehicleError(Exception):
    """Exception raised when an error occurs while fetching or parsing a SWAPI vehicle."""

    pass


class VehicleNotFoundError(SwapiVehicleError):
    """Exception raised when a vehicle is not found in SWAPI."""

    pass
