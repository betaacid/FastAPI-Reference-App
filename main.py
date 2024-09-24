from fastapi import FastAPI, status
from app.routers.characters_router import characters_router
from app.errors.exception_handlers import (
    swapi_character_error_handler,
    character_not_found_error_handler,
    not_found_error_handler,
    server_error_handler,
    index_out_of_range_error_handler,
)

from app.errors.custom_exceptions import (
    SwapiCharacterError,
    CharacterNotFoundError,
    VehicleNotFoundError,
    SwapiVehicleError,
)

app = FastAPI()

app.include_router(characters_router)

app.add_exception_handler(SwapiCharacterError, swapi_character_error_handler)
app.add_exception_handler(CharacterNotFoundError, character_not_found_error_handler)
app.add_exception_handler(VehicleNotFoundError, character_not_found_error_handler)
app.add_exception_handler(IndexError, index_out_of_range_error_handler)
app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_error_handler)
app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, server_error_handler)
