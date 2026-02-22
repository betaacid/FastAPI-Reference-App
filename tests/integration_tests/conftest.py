import pytest
from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from database import get_engine, get_db_session
from main import app


@pytest.fixture
def integration_client():
    engine = get_engine()
    conn = engine.connect()
    txn = conn.begin()
    session = Session(bind=conn)

    def override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as client:
        yield client

    txn.rollback()
    session.close()
    conn.close()
    app.dependency_overrides.clear()
