from http import HTTPStatus


def test_create_user(client):
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
