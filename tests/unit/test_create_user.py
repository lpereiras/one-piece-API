from http import HTTPStatus

# from one_piece_api.schemas.user_schema import UserSchema


def test_create_user(client):
    # test_user_schema = UserSchema.model_validate(test_user).model_dump()

    response = client.post(
        '/users/',
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


def test_create_user_with_existing_username(client):
    # test_user_schema = UserSchema.model_validate(test_user).model_dump()
    response = client.post(
        '/users/',
        json={
            'username': 'teste_username field',
            'email': 'teste_email.field@com.br',
            'password': 'teste_password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    response = client.post(
        '/users/',
        json={
            'username': 'teste_username field',
            'email': 'teste_email_valid.field@com.br',
            'password': 'teste_password',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'That username has already been claimed by another pirate.'
    }


def test_create_user_with_existing_email(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste_username field',
            'email': 'teste_email.field@com.br',
            'password': 'teste_password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    response = client.post(
        '/users/',
        json={
            'username': 'teste_username valid field',
            'email': 'teste_email.field@com.br',
            'password': 'teste_password',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'This email is already taken.'
    }
