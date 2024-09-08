class SwapiCharacterError(Exception):
    """Exception raised when an error occurs while fetching or parsing a SWAPI character."""

    pass


class CharacterNotFoundError(SwapiCharacterError):
    """Exception raised when a character is not found in SWAPI."""

    pass
