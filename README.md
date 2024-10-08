# FastAPI SWAPI Character Application

This project is a **reference architecture** for building FastAPI applications at [Beta Acid](https://betaacid.co). It demonstrates a clean, maintainable structure for a FastAPI app where users can enter a character name, which triggers a call to the [SWAPI API](https://swapi.dev) to fetch details about the character and store them in a database. Accompanying blog [post](https://betaacid.co/blog/introducing-our-clean-and-modular-fastapi-reference-architecture). 


## Table of Contents

- [FastAPI SWAPI Character Application](#fastapi-swapi-character-application)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Testing Strategy](#testing-strategy)
    - [Unit Tests](#unit-tests)
    - [Integration Tests](#integration-tests)
  - [Naming](#naming)
  - [Application Structure](#application-structure)
    - [Main File](#main-file)
    - [Router Files](#router-files)
    - [Service Layer](#service-layer)
    - [Clients](#clients)
    - [Domain Logic](#domain-logic)
    - [Utils](#utils)
  - [Installation and running](#installation-and-running)
  - [Running Tests](#running-tests)

## Project Overview

The application allows users to enter the name of a Star Wars character, which triggers the following steps:
1. A call is made to the SWAPI API to fetch the character's data.
2. The character's name is formatted.
3. The character data is stored in a database.


This project serves as a **reference architecture** to demonstrate best practices for organizing FastAPI projects, focusing on separation of concerns, testing strategies, and modularization. This project focuses on application architecture and does not cover CI/CD, deployment, Docker, or other operational best practices.

Note that type safety should be used whenever possible including parameters and return types. 

## Testing Strategy

The goal is to achieve **high test coverage** with mocked dependencies at every layer, ensuring that each component works in isolation.
****
### Unit Tests

- Each layer of the architecture (clients, services, routers, etc.) is tested individually.
- All dependencies, including external services like SWAPI and database calls, are mocked in unit tests.
- We only test **public methods** to avoid coupling tests to internal implementation details, 
- No external service calls are made during unit tests.

### Integration Tests
- Integration testing will be handled by the front end's end-to-end testing.
- In the case where we can not perform front end tests, use a **few integration tests**  to test the entire flow with real API calls and database interactions.
- These tests are minimal and only serve as sanity checks to ensure the app functions as expected in a real-world scenario.
- Integration tests ensure that the different layers of the architecture work together correctly.

## Naming
To ensure that the file names clearly describe their purpose, we follow a naming convention that reflects the functionality of each file. This helps maintain clarity, especially in larger projects. Here's how we structure the file names:

**Services**: These files coordinate the logic and interactions between external systems, databases, and internal business logic. We name them based on the service they provide. For example, instead of `service/character.py`, we would use `service/character_service.py`, making it clear that this file handles business logic related to Star Wars characters.

**Routers**: These files define the API endpoints. We include "router" in the file name to clarify that this file handles route definitions. Instead of `router/character.py`, we would name it `router/character_router.py`.

## Application Structure

The application is designed to be modular, with clear separation of concerns. Here's a breakdown of the main components:

### Main File

The `main.py` file serves as the entry point for the application. It initializes the FastAPI app, makes any app-wide configurations, and includes the necessary routers:

```python
from fastapi import FastAPI
from app.routers import characters_router

app = FastAPI()

app.include_router(characters_router)
```

### Router Files

The routers are responsible for defining the API routes. They remain very clean and only handles request validation and forwarding the call to the service layer:

```python
@characters_router.post("/", response_model=StarWarsCharacterRead)
async def create_character(
    input_character: StarWarsCharacterCreate, db: Session = Depends(get_db_session)
) -> StarWarsCharacterRead:
    return add_new_character(input_character, db)
```

### Service Layer

The service layer acts as the **main coordinator** of business logic. It handles calls to external services (SWAPI) and the database, formats the character name, and ensures data is processed correctly:

```python
def add_new_character(input_character: StarWarsCharacterCreate, db: Session) -> StarWarsCharacterRead:
    swapi_json = get_character_from_swapi(input_character.name)
    swapi_character = transform_swapi_character_json_to_pydantic(swapi_json)
    formatted_name = format_star_wars_name(swapi_character.name)
    swapi_character.name = formatted_name
    return insert_new_character(db, swapi_character)
```

### Clients

External dependencies such as SWAPI API calls and database operations are handled in the `clients` directory. Each client is responsible for interacting with a specific external system, ensuring clean separation of concerns.

For example, the `swapi_networking_client.py` handles SWAPI API interactions:

```python
def get_character_from_swapi(name: str) -> dict:
    response = requests.get(f"https://swapi.dev/api/people/?search={name}")
    response.raise_for_status()
    return response.json()
```

### Domain Logic

The domain logic is responsible for handling business rules and calculations. The domain logic ensures that the core business rules are applied consistently across the application.

For example, the `vehicle_calculations.py` file handles calculations related to vehicle efficiency:

```python
def convert_consumables_to_days(consumables: str) -> int:
```

### Utils

Utility functions are used for common tasks that are shared across different parts of the application. These functions are generally stateless and reusable.

For example, the `characters_utils.py` file contains a utility function for formatting Star Wars character names:

```python
def format_star_wars_name(name: str) -> str:
```

## Installation and running

To run the project locally, follow these steps:

1. Clone the repository:

2. Create and activate a virtual environment:

   - On macOS/Linux:

     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

   - On Windows:

     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:

   - Copy the `example.env` file and rename it to `.env`.
   - Edit the `.env` file to include your PostgreSQL connection information:

   ```
   DATABASE_URL=postgresql://<username>@localhost/star_wars
   ```

5. Set up the database (using Alembic for migrations):

   ```bash
   alembic upgrade head
   ```

6. Start the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

You can now visit `http://127.0.0.1:8000/docs` to interact with the API through the automatically generated Swagger UI.

## Running Tests

To run all tests, use the following command:

```bash
pytest
```

To run only the **unit tests**:

```bash
pytest tests/unit_tests/
```

To run the **integration tests**:

```bash
pytest tests/integration_tests/
```
