# FastAPI SWAPI Character Application

This is [Beta Acid](https://betaacid.co)'s reference architecture for FastAPI apps. Its a trivial app where you enter a Star Wars character name, the app fetches their details from the [SWAPI API](https://swapi.dev), and stores them in Postgres.

It's intentionally small. The point is to show how we like to structure things, not to build a real product. It covers application architecture only, not CI/CD, deployment, or Docker. Accompanying blog [post](https://betaacid.co/blog/introducing-our-clean-and-modular-fastapi-reference-architecture).

## How it's structured

```
Router  ->  Service  ->  Database Client  ->  Database
                \-> Networking Client  ->  SWAPI API
```

Each layer depends only on the one below it. FastAPI's `Depends` wires the chain together automatically, and all of that wiring lives in one place: `app/dependencies.py`. The services and clients themselves are plain Python classes that never import FastAPI:

```python
# Plain Python, no FastAPI imports
class CharactersService:
    def __init__(self, db_client: CharactersDatabaseClient, swapi_client: SwapiClient):
        self.db_client = db_client
        self.swapi_client = swapi_client
```

```python
# app/dependencies.py, the only file that knows about Depends
def get_characters_db_client(db: DbSession) -> CharactersDatabaseClient:
    return CharactersDatabaseClient(db)


def get_characters_service(
    db_client: Annotated[CharactersDatabaseClient, Depends(get_characters_db_client)],
    swapi_client: SwapiClientDep,
) -> CharactersService:
    return CharactersService(db_client, swapi_client)
```

```python
# Router only knows about the service
@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate,
    service: Annotated[CharactersService, Depends(get_characters_service)],
) -> StarWarsCharacterRead:
    return await service.add_new_character(input_character)
```

FastAPI resolves the whole chain for you: `router -> get_characters_service -> get_characters_db_client -> get_db_session`. The router never touches a db session, and the service never knows how the database client gets its connection. When testing, you can cut the chain at any level.

Nested dependencies don't require classes. `Depends` accepts any callable, and the providers above are plain functions. We use classes for services and clients because they hold injected state (`self.db_client`, `self.db`), not because the DI system demands it. If something holds injected dependencies or a resource like a session or an HTTP client, a class is a good fit. If it's pure calculation, formatting, or parsing, write a plain module function. That's what `app/domain/` and `app/utils/` are.

## Async by default

Every function that does I/O is `async` and gets awaited: routers, services, database clients, and the SWAPI client. The database uses SQLAlchemy's `AsyncSession` over `asyncpg`; HTTP calls use `httpx.AsyncClient`. Pure logic (`app/domain/`, `app/utils/`) stays as plain sync functions, since there's nothing to await.

Never block inside `async def`. An `async def` endpoint runs on the event loop itself, so a blocking call (`requests.get`, a sync SQLAlchemy query) freezes the whole server for every concurrent request. Either the whole call path is async, or the endpoint should be a plain `def` so FastAPI runs it in a threadpool. Don't mix.

The shared `httpx.AsyncClient` is created once at startup in `main.py`'s lifespan and closed at shutdown. It owns the connection pool, base URL, and timeout for all SWAPI calls.

## Transactions

The transaction boundary lives in `get_db_session`, not in the database clients. The session commits once the request handler finishes successfully and rolls back if it raises. Database clients only `add` and `flush`, so a request that writes multiple records stays atomic and no client ever has to decide whether it's safe to commit.

## Project layout

```
main.py                             # FastAPI app, lifespan, router registration, exception handlers
database.py                         # Async engine, session factory, get_db_session dependency

app/
  dependencies.py                   # All of the FastAPI Depends wiring
  routers/                          # API endpoints, thin, just validates and delegates
  services/                         # Business logic, coordinates between clients
  clients/
    database/                       # Database operations (the repository layer)
    networking/                     # External API calls (SWAPI)
  models/                           # SQLAlchemy ORM models
  schemas/                          # Pydantic request/response schemas
  domain/                           # Pure business rules (e.g. vehicle efficiency calc)
  utils/                            # Stateless helper functions
  errors/                           # Custom exceptions and exception handlers

tests/
  unit_tests/                       # Everything mocked; never touches the database or network
  integration_tests/                # Real Postgres, real SWAPI, transaction rollback
```

## Stack and layers

**Models and schemas.** SQLAlchemy ORM models (`app/models/`) map to Postgres tables. Pydantic schemas (`app/schemas/`) handle request validation and response serialization. There are two kinds of schemas: app-facing ones like `StarWarsCharacterCreate` / `StarWarsCharacterRead`, and SWAPI-facing ones like `SwapiCharacter` that represent the external API's response shape.

**Networking clients.** The networking client (`app/clients/networking/`) calls SWAPI through a shared `httpx.AsyncClient` and parses the JSON into Pydantic schemas. `SwapiClient` is a class because it holds real state (the HTTP client). The parsing functions next to it stay plain functions, since they're stateless JSON-to-Pydantic transforms. HTTP failures are wrapped into the app's own exceptions (`SwapiCharacterError`, `SwapiVehicleError`) at this boundary, so nothing above it knows or cares that httpx exists.

**Domain logic.** Pure business rules live in `app/domain/`. The vehicle efficiency calculation is an example: it takes a `SwapiVehicle` and returns a number, without touching the database or the network.

**Utils.** Stateless helpers like name formatting live in `app/utils/`. Same idea as domain logic, but more generic.

**Database.** Postgres over `asyncpg`, managed through Alembic migrations (which run over a plain sync connection; see `alembic/env.py`). The engine is created lazily in `database.py` so that importing the module doesn't require a `DATABASE_URL` to be set.

## Naming

File names say what they are. `characters_service.py`, not `characters.py`. `characters_router.py`, not `router.py`. When you have 30 files open, this matters.

## Testing

### Unit tests

Each layer is tested in isolation. The router tests override the service's provider function with `dependency_overrides`, and the service tests construct the class directly with mock clients. `@patch` is still used for plain functions like the JSON transforms, but the `Depends` chain eliminates it for anything in the DI graph. None of these tests touch a real database or the network; even the SWAPI client tests run against `httpx.MockTransport`.

```python
# Router test: override the provider function via FastAPI's DI
mock_service = MagicMock(spec=CharactersService)  # async methods become AsyncMocks
mock_service.add_new_character.return_value = mock_character
app.dependency_overrides[get_characters_service] = lambda: mock_service
```

```python
# Service test: construct directly, no FastAPI involved
mock_db_client = MagicMock(spec=CharactersDatabaseClient)
mock_swapi_client = MagicMock(spec=SwapiClient)
service = CharactersService(db_client=mock_db_client, swapi_client=mock_swapi_client)
result = await service.add_new_character(input_data)
```

Async tests run under `pytest-asyncio` in auto mode (configured in `pyproject.toml`), so an `async def` test works without any decorators or markers.

Unit tests don't need a `.env` file or a `DATABASE_URL`. The database engine is lazy (only created when actually used), so imports never trigger a connection.

### Integration tests

Integration tests hit real Postgres and real SWAPI. Each test's session rolls back instead of committing, so nothing persists.

The `integration_client` fixture in `tests/integration_tests/conftest.py` handles this. It overrides `get_db_session` with a version that rolls back where the real one would commit.

Integration tests require a `.env` with a valid `DATABASE_URL`.

## Setup

1. Clone the repo

2. Install [uv](https://docs.astral.sh/uv/) if you don't have it, then install dependencies:

```bash
uv sync
```

3. Copy `example.env` to `.env` and set your Postgres username:

```
DATABASE_URL=postgresql+asyncpg://<username>@localhost/star_wars
```

4. Create the database and run migrations:

```bash
createdb star_wars
uv run alembic upgrade head
```

5. Start the app:

```bash
uv run uvicorn main:app --reload
```

Then visit `http://127.0.0.1:8000/docs`.

## Running tests

Unit tests (no database required):

```bash
uv run pytest tests/unit_tests/ -v
```

Integration tests (requires `.env` with a valid database):

```bash
uv run pytest tests/integration_tests/ -v
```

Everything:

```bash
uv run pytest -v
```
