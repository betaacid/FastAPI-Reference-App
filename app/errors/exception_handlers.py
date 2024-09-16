from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.errors.custom_exceptions import SwapiCharacterError, CharacterNotFoundError


def swapi_character_error_handler(
    request: Request, exc: SwapiCharacterError
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "message": "An error occurred while fetching or parsing a SWAPI character."
        },
    )


def character_not_found_error_handler(
    request: Request, exc: CharacterNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": "Character not found in SWAPI."},
    )


def not_found_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"message": "Not Found"},
    )


def server_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


def index_out_of_range_error_handler(request: Request, exc: IndexError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": "Index out of range"},
    )
