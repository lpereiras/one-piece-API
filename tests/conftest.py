import pytest
from fastapi.testclient import TestClient

from one_piece_api.app import app


@pytest.fixture
def client():
    return TestClient(app)
