from http import HTTPStatus

from freezegun import freeze_time
from jwt import decode

from security import get_access_token
from settings import Settings


def test_get_access_token_with_success(client, test_user):
    response = client.post(
        '/auth/token', data={'username': test_user.username, 'password': test_user.clean_password}
    )
    access_token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert access_token['token_type'] == 'Bearer'
    assert 'access_token' in access_token


def test_get_access_token_add_expire():
    payload_data = {'sub': 'username.test'}
    token = get_access_token(payload_data)

    result = decode(token, key=Settings().SECRET_KEY, algorithms=Settings().ALGORITHM)

    assert result['sub'] == payload_data['sub']
    assert result['exp']


def test_get_access_token_with_invalid_username(client, test_user):
    response = client.post(
        '/auth/token', data={'username': 'username_invalid', 'password': test_user.clean_password}
    )

    invalid_access = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert invalid_access['detail'] == 'Invalid username or password'


def test_get_access_token_with_invalid_password(client, test_user):
    response = client.post(
        '/auth/token', data={'username': test_user.username, 'password': 'password_invalid'}
    )

    invalid_access = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert invalid_access['detail'] == 'Invalid username or password'


def test_token_when_expired(client, test_user):
    with freeze_time('1998-11-26 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': test_user.username, 'password': test_user.clean_password},
        )
        access_token = response.json()['access_token']
        print(access_token)
    with freeze_time('1998-11-26 12:31:00'):
        response = client.delete(
            f'/users/{test_user.id}',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
