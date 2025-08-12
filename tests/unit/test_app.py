from http import HTTPStatus

from fastapi.testclient import TestClient

from one_piece_api.app import app


def test_API_version_validate_version():
    client = TestClient(app)

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'version': 'v0.0.1'}
