from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'teste_username field',
            'email': 'teste_email.field@com.br',
            'password': 'teste_password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'teste_username field',
        'message': 'User successfully registered!',
    }
