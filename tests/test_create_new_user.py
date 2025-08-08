from http import HTTPStatus

from fastapi.testclient import TestClient

from one_piece_api.app import app


def test_create_new_user():
    client = TestClient(app)

    response = client.post('/one-piece-api/sign-up')
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'message': 'Usuário registrado com sucesso!'}
