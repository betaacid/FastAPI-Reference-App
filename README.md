# FastAPI SWAPI Character Application

This is [Beta Acid](https://betaacid.co)'s reference architecture for FastAPI apps. Its a trivial app where you enter a Star Wars character name, the app fetches their details from the [SWAPI API](https://swapi.dev), and stores them in Postgres.

It's intentionally small. The point is to show how we like to structure things, not to build a real product. It covers application architecture only -- not CI/CD, deployment, or Docker. Accompanying blog [post](https://betaacid.co/blog/introducing-our-clean-and-modular-fastapi-reference-architecture).

## How it's structured

```
Router  ->  Service  ->  Database Client  ->  Database
                \-> Networking Client  ->  SWAPI API
```

Each layer depends only on the one below it. FastAPI's `Depends` wires the chain together automatically:

- The **router** depends on a service class
- The **service** depends on a database client class
- The **database client** depends on the db session

```python
# Router only knows about the service
@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate,
    service: CharactersService = Depends(CharactersService),
) -> StarWarsCharacterRead:
    return service.add_new_character(input_character)
```

```python
# Service only knows about the database client
class CharactersService:
    def __init__(self, db_client: CharactersDatabaseClient = Depends(CharactersDatabaseClient)):
        self.db_client = db_client
```

```python
# Database client only knows about the session
class CharactersDatabaseClient:
    def __init__(self, db: Session = Depends(get_db_session)):
        self.db = db
```

FastAPI resolves this whole chain for you. The router never touches a db session, and the service never knows how the database client gets its connection. When testing, you can cut the chain at any level.

## Project layout

```
main.py                             # FastAPI app, router registration, exception handlers
database.py                         # Engine, session factory, get_db_session dependency

app/
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
  unit_tests/                       # No database, no network, everything mocked
  integration_tests/                # Real Postgres, real SWAPI, transaction rollback
```

## Stack and layers

**Models and schemas** -- SQLAlchemy ORM models (`app/models/`) map to Postgres tables. Pydantic schemas (`app/schemas/`) handle request validation and response serialization. There are two kinds of schemas: app-facing ones like `StarWarsCharacterCreate` / `StarWarsCharacterRead`, and SWAPI-facing ones like `SwapiCharacter` that represent the external API's response shape.

**Networking clients** -- The networking client (`app/clients/networking/`) calls SWAPI using `requests` and parses the JSON into Pydantic schemas. These are plain functions, not classes -- they're not part of the DI chain because they don't need a database session or any injected state.

**Domain logic** -- Pure business rules live in `app/domain/`. The vehicle efficiency calculation is an example: it takes a `SwapiVehicle` and returns a number. No database, no HTTP, no side effects.

**Utils** -- Stateless helpers like name formatting live in `app/utils/`. Same idea as domain logic, but more generic.

**Database** -- Postgres, managed through Alembic migrations. The engine is created lazily in `database.py` so that importing the module doesn't require a `DATABASE_URL` to be set.

## Naming

File names say what they are. `characters_service.py`, not `characters.py`. `characters_router.py`, not `router.py`. When you have 30 files open, this matters.

## Testing

### Unit tests

Each layer is tested in isolation. The router tests override the service with `dependency_overrides` (not `@patch`). The service tests construct the class directly with a mock database client. The database client tests pass in a mock session. No real database, no network calls.

```python
# Router test: override the service via FastAPI's DI
mock_service = MagicMock(spec=CharactersService)
mock_service.add_new_character.return_value = mock_character
app.dependency_overrides[CharactersService] = lambda: mock_service
```

```python
# Service test: construct directly, no FastAPI involved
mock_db_client = MagicMock(spec=CharactersDatabaseClient)
service = CharactersService(db_client=mock_db_client)
result = service.add_new_character(input_data)
```

Unit tests don't need a `.env` file or a `DATABASE_URL`. The database engine is lazy (only created when actually used), so imports never trigger a connection.

### Integration tests

Integration tests hit real Postgres and real SWAPI. Each test runs inside a database transaction that rolls back when the test finishes, so nothing persists.

The `integration_client` fixture in `tests/integration_tests/conftest.py` handles this. It overrides `get_db_session` with a session bound to an uncommitted transaction, then rolls it back in teardown.

Integration tests require a `.env` with a valid `DATABASE_URL`.

## Setup

1. Clone the repo

2. Install [uv](https://docs.astral.sh/uv/) if you don't have it, then install dependencies:

```bash
uv sync
```

3. Copy `example.env` to `.env` and set your Postgres username:

```
DATABASE_URL=postgresql://<username>@localhost/star_wars
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
