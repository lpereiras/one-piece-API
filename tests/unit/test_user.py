from http import HTTPStatus

from fastapi.testclient import TestClient

from one_piece_api.app import app


def test_create_user():
    client = TestClient(app)

    response = client.post(
        '/one-piece-api/sign-up',
        json={
            'username': 'teste_username field',
            'email': 'teste_email.field@com.br',
            'password': 'teste_password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste_username field',
        'message': 'Usuário registrado com sucesso!',
    }
