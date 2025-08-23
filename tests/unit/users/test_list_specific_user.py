from http import HTTPStatus

from one_piece_api.schemas.user_schema import UserPublic


def test_list_specific_user(client, test_user):
    test_user_schema = UserPublic.model_validate(test_user).model_dump()

    response = client.get(f'/users/{test_user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == test_user_schema


def test_list_users_invalid_search(client):
    response = client.get(f'/users/{0}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'There is nothing to see here. Or are you searching for '
        'someone from the Void Century?'
    }
