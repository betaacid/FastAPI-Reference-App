# FastAPI SWAPI Character Application

This is [Beta Acid](https://betaacid.co)'s reference architecture for FastAPI apps. Its a trivial app where you enter a Star Wars character name, the app fetches their details from the [SWAPI API](https://swapi.dev), and stores them in Postgres.

It's intentionally small. The point is to show how we like to structure things, not to build a real product. It covers application architecture only, not CI/CD, deployment, or Docker. Accompanying blog [post](https://betaacid.co/blog/introducing-our-clean-and-modular-fastapi-reference-architecture).

## How it's structured

```
Router  ->  Service  ->  Database Client  ->  Database
                \-> Networking Client  ->  SWAPI API
```

Each layer depends only on the one below it. Services and database clients are module-level functions that receive their dependencies as plain arguments, the same style used by FastAPI's official [full-stack template](https://github.com/fastapi/full-stack-fastapi-template) and [Netflix Dispatch](https://github.com/Netflix/dispatch). FastAPI's `Depends` appears only at the edge: the router injects a database session and the SWAPI client, then passes them down.

```python
# Router: inject the session and the SWAPI client, delegate to the service
@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate,
    db: DbSession,
    swapi_client: SwapiClientDep,
) -> StarWarsCharacterRead:
    return await characters_service.add_new_character(input_character, db, swapi_client)
```

```python
# Service: a plain async function, no FastAPI imports
async def add_new_character(
    input_character: StarWarsCharacterCreate,
    db: AsyncSession,
    swapi_client: SwapiClient,
) -> StarWarsCharacterRead:
    swapi_json = await swapi_client.get_character(input_character.name)
    ...
```

The `DbSession` and `SwapiClientDep` annotations live in `app/dependencies.py`, the only file that knows about `Depends`. The SWAPI client is itself built through a nested dependency chain (`router -> get_swapi_client -> get_http_client`), so the router never learns where the shared HTTP client comes from.

Nested dependencies don't require classes. `Depends` accepts any callable, and `get_db_session`, `get_http_client`, and `get_swapi_client` are all plain functions. The one class in the request path is `SwapiClient`, and it earns that by holding real state: the shared `httpx.AsyncClient` with its connection pool, base URL, and timeout. That's the rule throughout the app. A class needs genuine state or a resource to manage; everything else, including business logic, is a module function.

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

Each layer is tested in isolation. Injected dependencies get swapped through `dependency_overrides` (the shared `client` fixture replaces `get_db_session` with a mock session), and plain functions get mocked with `@patch`. None of these tests touch a real database or the network; even the SWAPI client tests run against `httpx.MockTransport`.

```python
# Router test: patch the service function the router delegates to
@patch("app.services.characters_service.add_new_character", new_callable=AsyncMock)
def test_create_character_valid_data(mock_add_new_character, client, mock_character):
    mock_add_new_character.return_value = mock_character
    response = client.post("/characters/", json={"name": "Darth Vader"})
```

```python
# Service test: call the function directly, no FastAPI involved
mock_swapi_client = MagicMock(spec=SwapiClient)  # async methods become AsyncMocks
result = await add_new_character(input_data, mock_db_session, mock_swapi_client)
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
