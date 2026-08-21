import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repository import task_repository


@pytest.fixture(autouse=True)
def reset_repository():
    """Ensure each test starts with a clean in-memory store."""
    task_repository._tasks.clear()
    task_repository._id_counter = __import__("itertools").count(start=1)
    yield


@pytest.fixture
def client():
    return TestClient(app)
