from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.db import get_engine
from app.main import app

client = TestClient(app)


@pytest.fixture
def unreachable_database() -> Iterator[None]:
    broken_engine = create_engine("postgresql+psycopg://user:pass@127.0.0.1:1/none")
    app.dependency_overrides[get_engine] = lambda: broken_engine
    yield
    app.dependency_overrides.clear()


def test_readiness_ok_when_database_is_reachable() -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.usefixtures("unreachable_database")
def test_readiness_unavailable_when_database_is_down() -> None:
    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}
